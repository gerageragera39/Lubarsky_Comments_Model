"""
Main GUI application for the YouTube Comment Classifier
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, Any

from .config import Config
from .models import Sentiment
from .api_client import YouTubeAPIClient
from .dataset_manager import DatasetManager
from .session_manager import SessionManager
from .classifier_controller import ClassifierController
from .utils import extract_video_id
from .gui_constants import COLORS, FONT_FAMILY, KEY_BINDINGS


class CommentClassifierApp(tk.Tk):
    """Main GUI application for YouTube comment classification"""
    
    def __init__(self):
        super().__init__()
        self.title("YouTube Comment Classifier")
        self.geometry("920x720")
        self.minsize(800, 640)
        self.configure(bg=COLORS["bg_dark"])
        
        # Initialize managers and controller
        self.dataset_manager = DatasetManager(Config.DATASET_FILE)
        self.session_manager = SessionManager(Config.SESSION_FILE)
        self.controller = ClassifierController(self.dataset_manager, self.session_manager)
        
        # Setup UI
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        self.container = tk.Frame(self, bg=COLORS["bg_dark"])
        self.container.pack(fill="both", expand=True)
        
        # Start with the initial screen
        self._build_start_screen()
    
    def _make_button(self, parent, text, bg, hover_bg, fg="white", command=None,
                     width=14, height=2, font_size=12):
        """Create a styled button"""
        btn = tk.Button(
            parent, text=text, bg=bg, fg=fg,
            activebackground=hover_bg, activeforeground=fg,
            font=(FONT_FAMILY, font_size, "bold"),
            width=width, height=height, bd=0,
            cursor="hand2", relief="flat", command=command,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn
    
    def _clear(self):
        """Clear the container of all widgets"""
        for widget in self.container.winfo_children():
            widget.destroy()
        for key in (KEY_BINDINGS["positive"] + 
                   KEY_BINDINGS["neutral"] + 
                   KEY_BINDINGS["negative"] +
                   KEY_BINDINGS["skip"] +
                   KEY_BINDINGS["back"] +
                   KEY_BINDINGS["quit"]):
            self.unbind(key)
    
    # ==================== SCREEN 0: START ====================
    def _build_start_screen(self):
        """Build the start screen"""
        self._clear()
        if self.session_manager.has_active_session():
            self._build_choice_screen()
        else:
            self._build_url_screen()
    
    # ==================== SCREEN CHOICE ====================
    def _build_choice_screen(self):
        """Build the session choice screen"""
        self._clear()
        frame = self.container
        info = self.session_manager.get_session_info()

        tk.Label(
            frame, text="▶  YouTube Comment Classifier",
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
            font=(FONT_FAMILY, 22, "bold"),
        ).pack(pady=(40, 4))

        tk.Label(
            frame, text="Обнаружена незавершённая сессия классификации",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
            font=(FONT_FAMILY, 12),
        ).pack(pady=(0, 28))

        card = tk.Frame(frame, bg=COLORS["bg_card"], bd=0,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(padx=80, fill="x")

        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=30, pady=24, fill="x")

        tk.Label(inner, text="📹  Видео", bg=COLORS["bg_card"],
                 fg=COLORS["text_secondary"], font=(FONT_FAMILY, 9)).pack(anchor="w")

        url_display = info["video_url"]
        if len(url_display) > 70:
            url_display = url_display[:70] + "..."
        tk.Label(inner, text=url_display, bg=COLORS["bg_card"],
                 fg=COLORS["text_primary"], font=(FONT_FAMILY, 11)).pack(anchor="w", pady=(2, 12))

        prog_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        prog_frame.pack(fill="x", pady=(0, 6))

        for label, value, color in [
            ("Всего", str(info["total"]), COLORS["text_primary"]),
            ("Обработано", str(info["done"]), COLORS["positive"]),
            ("Осталось", str(info["remaining"]), COLORS["skip"]),
        ]:
            col = tk.Frame(prog_frame, bg=COLORS["bg_card"])
            col.pack(side="left", padx=(0, 30))
            tk.Label(col, text=value, bg=COLORS["bg_card"],
                     fg=color, font=(FONT_FAMILY, 20, "bold")).pack()
            tk.Label(col, text=label, bg=COLORS["bg_card"],
                     fg=COLORS["text_secondary"], font=(FONT_FAMILY, 9)).pack()

        ratio = info["done"] / max(info["total"], 1)
        bar_frame = tk.Frame(inner, bg=COLORS["progress_bg"], height=10)
        bar_frame.pack(fill="x", pady=(8, 0))
        bar_frame.update_idletasks()
        tk.Frame(bar_frame, bg=COLORS["accent"], height=10).place(
            relx=0, rely=0, relwidth=ratio, relheight=1.0)

        btn_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        btn_frame.pack(pady=(28, 0))

        self._make_button(btn_frame, "▶  Продолжить",
                          COLORS["resume"], COLORS["resume_hover"],
                          command=self._on_resume, width=22, height=2, font_size=12).pack(pady=(0, 12))
        self._make_button(btn_frame, "🔗  Новое видео",
                          COLORS["accent"], COLORS["accent_hover"],
                          command=self._on_new_video, width=22, height=2, font_size=12).pack(pady=(0, 12))
        self._make_button(btn_frame, "🗑  Удалить сессию",
                          COLORS["negative"], COLORS["negative_hover"],
                          command=self._on_delete_session, width=22, height=2, font_size=11).pack()

        stats_f = tk.Frame(frame, bg=COLORS["bg_dark"])
        stats_f.pack(side="bottom", pady=18)
        c = self.dataset_manager.get_counts()
        tk.Label(stats_f,
                 text=(f"📊  Датасет: {c['total']} комментариев  |  "
                       f"✅ {c['positive']}  ⚪ {c['neutral']}  🔴 {c['negative']}"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
                 font=(FONT_FAMILY, 10)).pack()

    def _on_resume(self):
        """Handle resume session action"""
        self.controller.resume_session()
        self._build_classify_screen()

    def _on_new_video(self):
        """Handle new video action"""
        self._build_url_screen()

    def _on_delete_session(self):
        """Handle delete session action"""
        if messagebox.askyesno("Удалить сессию",
                               "Удалить незавершённую сессию?\n"
                               "(Датасет dataset.csv НЕ будет затронут)"):
            self.session_manager.delete_session()
            self._build_url_screen()

    # ==================== SCREEN 1: URL ====================
    def _build_url_screen(self):
        """Build the URL input screen"""
        self._clear()
        frame = self.container

        tk.Label(frame, text="▶  YouTube Comment Classifier",
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
                 font=(FONT_FAMILY, 22, "bold")).pack(pady=(40, 4))
        tk.Label(frame, text="Вставьте ссылку на YouTube видео для загрузки комментариев",
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
                 font=(FONT_FAMILY, 11)).pack(pady=(0, 30))

        card = tk.Frame(frame, bg=COLORS["bg_card"], bd=0,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(padx=60, fill="x")
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=30, pady=30, fill="x")

        tk.Label(inner, text="URL видео", bg=COLORS["bg_card"],
                 fg=COLORS["text_secondary"], font=(FONT_FAMILY, 10)).pack(anchor="w")

        self.url_var = tk.StringVar()
        entry = tk.Entry(inner, textvariable=self.url_var, font=(FONT_FAMILY, 13),
                         bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                         insertbackground=COLORS["text_primary"], bd=0,
                         highlightthickness=1, highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["accent"])
        entry.pack(fill="x", pady=(6, 18), ipady=8)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self._on_fetch())

        self._make_button(inner, "⬇  Загрузить комментарии",
                          COLORS["accent"], COLORS["accent_hover"],
                          command=self._on_fetch, width=28, height=2, font_size=12).pack()

        if self.session_manager.has_active_session():
            back_f = tk.Frame(frame, bg=COLORS["bg_dark"])
            back_f.pack(pady=(14, 0))
            self._make_button(back_f, "← Назад к сессии",
                              COLORS["bg_card"], COLORS["border"],
                              fg=COLORS["text_secondary"],
                              command=self._build_choice_screen,
                              width=20, height=1, font_size=10).pack()

        self.status_var = tk.StringVar(value="")
        tk.Label(frame, textvariable=self.status_var, bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"], font=(FONT_FAMILY, 10)).pack(pady=(16, 0))
        self.progress = ttk.Progressbar(frame, mode="indeterminate", length=300)

        stats_f = tk.Frame(frame, bg=COLORS["bg_dark"])
        stats_f.pack(side="bottom", pady=18)
        c = self.dataset_manager.get_counts()
        tk.Label(stats_f,
                 text=(f"📊  Датасет: {c['total']} комментариев  |  "
                       f"✅ {c['positive']}  ⚪ {c['neutral']}  🔴 {c['negative']}"),
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
                 font=(FONT_FAMILY, 10)).pack()

    def _on_fetch(self):
        """Handle fetch comments action"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Ошибка", "Введите ссылку на видео")
            return
        video_id = extract_video_id(url)
        if not video_id:
            messagebox.showerror("Ошибка", "Не удалось извлечь ID видео из ссылки")
            return

        self.status_var.set("⏳ Загрузка комментариев...")
        self.progress.pack(pady=(6, 0))
        self.progress.start(12)
        self._fetching_url = url
        self._fetching_video_id = video_id

        def worker():
            try:
                client = YouTubeAPIClient(Config.API_KEY)
                comments = client.fetch_comments(video_id, Config.MAX_COMMENTS)
                self.after(0, lambda: self._on_fetched(comments))
            except Exception as exc:
                self.after(0, lambda exc=exc: self._on_fetch_error(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_fetch_error(self, msg: str):
        """Handle fetch error"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_var.set("")
        messagebox.showerror("Ошибка загрузки", msg)

    def _on_fetched(self, comments: list[str]):
        """Handle successful fetch"""
        self.progress.stop()
        self.progress.pack_forget()
        if not comments:
            self.status_var.set("Комментарии не найдены")
            return
        self.session_manager.create_session(self._fetching_url, self._fetching_video_id, comments)
        self.controller.start_new_session(comments)
        self._build_classify_screen()

    # ==================== SCREEN 2: CLASSIFICATION ====================
    def _build_classify_screen(self):
        """Build the classification screen"""
        self._clear()
        frame = self.container

        # --- 1. Top panel ---
        top_bar = tk.Frame(frame, bg=COLORS["bg_dark"])
        top_bar.pack(side="top", fill="x", padx=20, pady=(14, 0))

        tk.Label(top_bar, text="Классификация комментариев",
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
                 font=(FONT_FAMILY, 18, "bold")).pack(side="left")

        stats_card = tk.Frame(top_bar, bg=COLORS["bg_card"], bd=0,
                              highlightthickness=1, highlightbackground=COLORS["border"])
        stats_card.pack(side="right")
        self.stats_inner = tk.Frame(stats_card, bg=COLORS["bg_card"])
        self.stats_inner.pack(padx=12, pady=6)
        self._refresh_stats_panel()

        # --- 2. Progress ---
        prog_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        prog_frame.pack(side="top", fill="x", padx=24, pady=(12, 0))

        self.progress_text_var = tk.StringVar()
        tk.Label(prog_frame, textvariable=self.progress_text_var,
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
                 font=(FONT_FAMILY, 10)).pack(side="left")

        self.prog_canvas = tk.Canvas(prog_frame, height=8,
                                     bg=COLORS["progress_bg"], highlightthickness=0)
        self.prog_canvas.pack(side="right", fill="x", expand=True, padx=(12, 0))
        self.prog_canvas.bind("<Configure>", lambda e: self._draw_progress())

        # --- 3. BOTTOM BLOCK (buttons) — pack BOTTOM first ---
        bottom_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        bottom_frame.pack(side="bottom", fill="x", padx=24, pady=(0, 12))

        # Keyboard hints
        tk.Label(
            bottom_frame,
            text="Клавиши:  1 = Positive  |  2 = Neutral  |  3 = Negative  |  S = Skip  |  Z = Назад  |  Q = Выход",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
            font=(FONT_FAMILY, 9),
        ).pack(side="bottom", pady=(6, 0))

        # Rating buttons
        btn_container = tk.Frame(bottom_frame, bg=COLORS["bg_dark"])
        btn_container.pack(side="bottom", pady=(10, 0))

        buttons_data = [
            ("✅  Positive",  COLORS["positive"], COLORS["positive_hover"], lambda: self._classify(Sentiment.POSITIVE)),
            ("⚪  Neutral",   COLORS["neutral"],  COLORS["neutral_hover"],  lambda: self._classify(Sentiment.NEUTRAL)),
            ("🔴  Negative",  COLORS["negative"], COLORS["negative_hover"], lambda: self._classify(Sentiment.NEGATIVE)),
            ("⏭  Skip",       COLORS["skip"],     COLORS["skip_hover"],     self._skip),
        ]
        for i, (text, bg, hover, cmd) in enumerate(buttons_data):
            self._make_button(btn_container, text, bg, hover,
                              command=cmd, width=14, height=2, font_size=11
                              ).grid(row=0, column=i, padx=6)

        # Back button — separate row under main buttons
        nav_container = tk.Frame(bottom_frame, bg=COLORS["bg_dark"])
        nav_container.pack(side="bottom", pady=(10, 0))

        self.back_btn = self._make_button(
            nav_container, "↩  Назад (изменить предыдущий)",
            COLORS["back"], COLORS["back_hover"],
            command=self._go_back, width=30, height=1, font_size=10,
        )
        self.back_btn.pack(side="left", padx=(0, 16))

        self._make_button(
            nav_container, "💾  Сохранить и выйти",
            COLORS["bg_card"], COLORS["border"],
            fg=COLORS["text_secondary"],
            command=self._on_save_and_exit, width=20, height=1, font_size=10,
        ).pack(side="left")

        # --- Re-edit mode indicator ---
        self.reedit_label_var = tk.StringVar(value="")
        self.reedit_label = tk.Label(
            bottom_frame, textvariable=self.reedit_label_var,
            bg=COLORS["bg_dark"], fg=COLORS["back"],
            font=(FONT_FAMILY, 10, "bold"),
        )
        self.reedit_label.pack(side="bottom", pady=(8, 0))

        # --- 4. MIDDLE (comment card) ---
        middle_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
        middle_frame.pack(side="top", fill="both", expand=True, padx=24, pady=(12, 8))

        comment_card = tk.Frame(middle_frame, bg=COLORS["bg_card"], bd=0,
                                highlightthickness=1, highlightbackground=COLORS["border"])
        comment_card.pack(fill="both", expand=True)

        self.comment_number_var = tk.StringVar()
        tk.Label(comment_card, textvariable=self.comment_number_var,
                 bg=COLORS["bg_card"], fg=COLORS["accent"],
                 font=(FONT_FAMILY, 10, "bold")).pack(anchor="w", padx=20, pady=(12, 0))

        text_frame = tk.Frame(comment_card, bg=COLORS["bg_card"])
        text_frame.pack(fill="both", expand=True, padx=20, pady=(6, 14))

        self.comment_text = tk.Text(
            text_frame, wrap="word", bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            font=(FONT_FAMILY, 13), bd=0, highlightthickness=0,
            padx=4, pady=4, state="disabled", cursor="arrow",
            selectbackground=COLORS["accent"],
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical",
                                  command=self.comment_text.yview)
        self.comment_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.comment_text.pack(side="left", fill="both", expand=True)

        # Hotkeys
        for key in KEY_BINDINGS["positive"]:
            self.bind(key, lambda e: self._classify(Sentiment.POSITIVE))
        for key in KEY_BINDINGS["neutral"]:
            self.bind(key, lambda e: self._classify(Sentiment.NEUTRAL))
        for key in KEY_BINDINGS["negative"]:
            self.bind(key, lambda e: self._classify(Sentiment.NEGATIVE))
        for key in KEY_BINDINGS["skip"]:
            self.bind(key, lambda e: self._skip())
        for key in KEY_BINDINGS["back"]:
            self.bind(key, lambda e: self._go_back())
        for key in KEY_BINDINGS["quit"]:
            self.bind(key, lambda e: self._on_save_and_exit())

        self._update_back_button_state()
        self._show_comment()

    # ---------- Rendering ----------
    def _refresh_stats_panel(self):
        """Refresh the stats panel"""
        for widget in self.stats_inner.winfo_children():
            widget.destroy()
        
        c = self.dataset_manager.get_counts()
        tk.Label(
            self.stats_inner,
            text=(f"📊  Датасет: {c['total']}  |  "
                  f"✅ {c['positive']}  ⚪ {c['neutral']}  🔴 {c['negative']}"),
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
            font=(FONT_FAMILY, 10)
        ).pack()

    def _draw_progress(self):
        """Draw the progress bar"""
        self.prog_canvas.delete("all")
        width = self.prog_canvas.winfo_width()
        if width <= 1:
            width = 300  # fallback width
        
        current, total = self.controller.get_progress()
        if total == 0:
            ratio = 0
        else:
            ratio = current / total
        
        fill_width = int(width * ratio)
        self.prog_canvas.create_rectangle(0, 0, fill_width, 8, fill=COLORS["accent"], outline=COLORS["accent"])
        self.prog_canvas.create_rectangle(fill_width, 0, width, 8, fill=COLORS["progress_bg"], outline=COLORS["progress_bg"])
        
        self.progress_text_var.set(f"{current} / {total} ({ratio*100:.1f}%)")

    def _update_back_button_state(self):
        """Update the state of the back button"""
        if self.controller.can_go_back and self.controller.went_back_from is None:
            self.back_btn.config(state="normal")
        else:
            self.back_btn.config(state="disabled")

    def _show_comment(self):
        """Show the current comment"""
        comment = self.controller.get_current_comment()
        if comment:
            # Update comment number
            current, total = self.controller.get_progress()
            self.comment_number_var.set(f"КОММЕНТАРИЙ #{current + 1} ИЗ {total}")
            
            # Update comment text
            self.comment_text.config(state="normal")
            self.comment_text.delete(1.0, tk.END)
            self.comment_text.insert(1.0, comment.text)
            self.comment_text.config(state="disabled")
            
            # Update progress bar
            self._draw_progress()
            
            # Update back button state
            self._update_back_button_state()
            
            # Clear re-edit indicator if we moved forward after going back
            if self.controller.went_back_from is not None and self.controller.current_index > self.controller.went_back_from:
                self.reedit_label_var.set("")
                self.controller.went_back_from = None
        else:
            # No more comments
            self.comment_number_var.set("Все комментарии обработаны!")
            self.comment_text.config(state="normal")
            self.comment_text.delete(1.0, tk.END)
            self.comment_text.insert(1.0, "Все комментарии в этой сессии были обработаны.")
            self.comment_text.config(state="disabled")
            
            # Disable classification buttons
            for child in self.container.winfo_children():
                if isinstance(child, tk.Frame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, tk.Frame):
                            for great_grandchild in grandchild.winfo_children():
                                if isinstance(great_grandchild, tk.Button):
                                    btn_text = great_grandchild.cget("text")
                                    if btn_text in ["✅  Positive", "⚪  Neutral", "🔴  Negative", "⏭  Skip"]:
                                        great_grandchild.config(state="disabled")

    # ---------- Actions ----------
    def _classify(self, sentiment: Sentiment):
        """Classify the current comment with the given sentiment"""
        if self.controller.has_more_comments():
            self.controller.classify_current_comment(sentiment)
            self._show_comment()
            self._refresh_stats_panel()
        else:
            messagebox.showinfo("Информация", "Больше нет комментариев для классификации")

    def _skip(self):
        """Skip the current comment"""
        if self.controller.has_more_comments():
            self.controller.skip_current_comment()
            self._show_comment()
        else:
            messagebox.showinfo("Информация", "Больше нет комментариев для пропуска")

    def _go_back(self):
        """Go back to the previous comment"""
        if self.controller.go_back():
            self.reedit_label_var.set("РЕЖИМ ПЕРЕОЦЕНКИ: измените предыдущий комментарий")
            self._show_comment()
        else:
            messagebox.showinfo("Информация", "Невозможно вернуться назад")

    def _on_save_and_exit(self):
        """Save and exit the application"""
        self.controller.save_and_exit()
        self.destroy()


def main():
    """Main entry point"""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return
    
    app = CommentClassifierApp()
    app.mainloop()


if __name__ == "__main__":
    main()