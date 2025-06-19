import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import json
import os
from datetime import datetime
import threading
import time
import random


class ModernNotesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AldiyarZ Pro")
        self.root.geometry("1400x900")
        self.root.resizable(False, False)  # Фиксированный размер окна
        
        # Центрирование окна
        self.center_window()
        
        # Темы приложения
        self.themes = {
            'dark': {
                'name': 'Темная',
                'bg_primary': '#1a1a1a',
                'bg_secondary': '#2d2d2d',
                'bg_card': '#3a3a3a',
                'accent': '#6366f1',
                'accent_hover': '#4f46e5',
                'text_primary': '#ffffff',
                'text_secondary': '#a1a1aa',
                'border': '#4a4a4a',
                'success': '#22c55e',
                'warning': '#f59e0b',
                'danger': '#ef4444'
            },
            'light': {
                'name': 'Светлая',
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_card': '#ffffff',
                'accent': '#0066cc',
                'accent_hover': '#0052a3',
                'text_primary': '#1a1a1a',
                'text_secondary': '#6c757d',
                'border': '#dee2e6',
                'success': '#198754',
                'warning': '#fd7e14',
                'danger': '#dc3545'
            },
            'purple': {
                'name': 'Фиолетовая',
                'bg_primary': '#1a0d26',
                'bg_secondary': '#2d1b3d',
                'bg_card': '#3d2954',
                'accent': '#8b5cf6',
                'accent_hover': '#7c3aed',
                'text_primary': '#ffffff',
                'text_secondary': '#c4b5fd',
                'border': '#6d28d9',
                'success': '#10b981',
                'warning': '#f59e0b',
                'danger': '#ef4444'
            },
            'ocean': {
                'name': 'Океан',
                'bg_primary': '#0f172a',
                'bg_secondary': '#1e293b',
                'bg_card': '#334155',
                'accent': '#0ea5e9',
                'accent_hover': '#0284c7',
                'text_primary': '#f1f5f9',
                'text_secondary': '#94a3b8',
                'border': '#475569',
                'success': '#22c55e',
                'warning': '#f59e0b',
                'danger': '#ef4444'
            },
            'forest': {
                'name': 'Лес',
                'bg_primary': '#0d1b0d',
                'bg_secondary': '#1a2e1a',
                'bg_card': '#2d4a2d',
                'accent': '#22c55e',
                'accent_hover': '#16a34a',
                'text_primary': '#f0fdf4',
                'text_secondary': '#86efac',
                'border': '#166534',
                'success': '#22c55e',
                'warning': '#f59e0b',
                'danger': '#ef4444'
            }
        }
        
        # Загрузка настроек
        self.settings = self.load_settings()
        self.current_theme = self.settings.get('theme', 'dark')
        self.colors = self.themes[self.current_theme]
        
        self.notes = []
        self.current_note = None
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_notes)
        
        # Статистика
        self.stats = {
            'total_notes': 0,
            'total_words': 0,
            'session_start': datetime.now()
        }
        
        self.setup_styles()
        self.create_ui()
        self.load_notes()
        self.start_autosave()
        self.start_motivational_quotes()
        
        # Горячие клавиши
        self.setup_hotkeys()
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 1400
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Настройка современных стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Основные стили
        style.configure('Modern.TFrame', background=self.colors['bg_primary'])
        style.configure('Card.TFrame', background=self.colors['bg_card'], relief='flat')
        style.configure('Sidebar.TFrame', background=self.colors['bg_secondary'])
        
    def create_ui(self):
        """Создание современного пользовательского интерфейса"""
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Главный контейнер
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Создание панелей
        self.create_sidebar(main_frame)
        self.create_main_area(main_frame)
        
    def create_sidebar(self, parent):
        """Создание боковой панели с заметками"""
        sidebar = tk.Frame(parent, bg=self.colors['bg_secondary'], width=380)
        sidebar.pack(side='left', fill='y', padx=(0, 2))
        sidebar.pack_propagate(False)
        
        # Заголовок и поиск
        header_frame = self.create_header(sidebar)
        
        # Статистика
        self.create_stats_panel(sidebar)
        
        # Кнопки действий
        self.create_action_buttons(sidebar)
        
        # Список заметок
        self.create_notes_list(sidebar)
        
        # Настройки внизу
        self.create_settings_panel(sidebar)
        
    def create_header(self, parent):
        """Создание заголовка"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill='x', pady=(20, 10), padx=20)
        header_frame.pack_propagate(False)
        
        # Анимированный заголовок
        title_label = tk.Label(header_frame, text="✨ ZametkaAldiyara Pro", 
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(15, 10))
        
        # Поле поиска с иконкой
        search_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        search_frame.pack(fill='x')
        
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=('Segoe UI', 11),
                                    bg=self.colors['bg_card'],
                                    fg=self.colors['text_primary'],
                                    insertbackground=self.colors['text_primary'],
                                    relief='flat', bd=10)
        self.search_entry.pack(fill='x', ipady=10)
        self.search_entry.insert(0, "🔍 Найти заметку...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        return header_frame
        
    def create_stats_panel(self, parent):
        """Создание панели статистики"""
        stats_frame = tk.Frame(parent, bg=self.colors['bg_card'], height=80)
        stats_frame.pack(fill='x', pady=10, padx=20)
        stats_frame.pack_propagate(False)
        
        # Статистика в строку
        stats_container = tk.Frame(stats_frame, bg=self.colors['bg_card'])
        stats_container.pack(expand=True, fill='both', pady=15)
        
        # Количество заметок
        notes_frame = tk.Frame(stats_container, bg=self.colors['bg_card'])
        notes_frame.pack(side='left', expand=True, fill='x')
        
        self.notes_count_label = tk.Label(notes_frame, text="0", 
                                         font=('Segoe UI', 16, 'bold'),
                                         bg=self.colors['bg_card'],
                                         fg=self.colors['accent'])
        self.notes_count_label.pack()
        
        tk.Label(notes_frame, text="Заметок", 
                font=('Segoe UI', 9),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack()
        
        # Количество слов
        words_frame = tk.Frame(stats_container, bg=self.colors['bg_card'])
        words_frame.pack(side='left', expand=True, fill='x')
        
        self.words_count_label = tk.Label(words_frame, text="0", 
                                         font=('Segoe UI', 16, 'bold'),
                                         bg=self.colors['bg_card'],
                                         fg=self.colors['success'])
        self.words_count_label.pack()
        
        tk.Label(words_frame, text="Слов", 
                font=('Segoe UI', 9),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack()
        
    def create_action_buttons(self, parent):
        """Создание кнопок действий"""
        buttons_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill='x', pady=10, padx=20)
        
        # Главная кнопка создания заметки
        self.new_note_btn = tk.Button(buttons_frame, text="🖊 Новая заметка",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['accent'],
                                     fg=self.colors['text_primary'],
                                     relief='flat', bd=0,
                                     cursor='hand2',
                                     command=self.create_new_note)
        self.new_note_btn.pack(fill='x', ipady=15)
        self.new_note_btn.bind('<Enter>', lambda e: self.button_hover(e, True))
        self.new_note_btn.bind('<Leave>', lambda e: self.button_hover(e, False))
        
        # Дополнительные кнопки
        extra_buttons_frame = tk.Frame(buttons_frame, bg=self.colors['bg_secondary'])
        extra_buttons_frame.pack(fill='x', pady=(10, 0))
        
        extra_buttons = [
            ("📋 Шаблон", self.create_template_note),
            ("🎲 Случайная", self.open_random_note)
        ]
        
        for i, (text, command) in enumerate(extra_buttons):
            btn = tk.Button(extra_buttons_frame, text=text,
                           font=('Segoe UI', 10),
                           bg=self.colors['bg_card'],
                           fg=self.colors['text_primary'],
                           relief='flat', bd=0,
                           cursor='hand2',
                           command=command)
            btn.pack(side='left' if i == 0 else 'right', 
                    fill='x', expand=True,
                    padx=(0, 5) if i == 0 else (5, 0),
                    ipady=10)
            btn.bind('<Enter>', lambda e: self.tool_button_hover(e, True))
            btn.bind('<Leave>', lambda e: self.tool_button_hover(e, False))
            
    def create_notes_list(self, parent):
        """Создание списка заметок с горизонтальным и вертикальным скроллбаром"""
        notes_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        notes_frame.pack(fill='both', expand=True, padx=20, pady=(10, 0))
        
        # Заголовок списка
        list_header = tk.Frame(notes_frame, bg=self.colors['bg_secondary'], height=30)
        list_header.pack(fill='x', pady=(0, 10))
        list_header.pack_propagate(False)
        
        tk.Label(list_header, text="📝 Мои заметки",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).pack(side='left', pady=5)
        
        # Контейнер для канваса с двумя скроллбарами
        canvas_frame = tk.Frame(notes_frame, bg=self.colors['bg_secondary'])
        canvas_frame.pack(fill='both', expand=True)

        # Создаём канвас
        canvas = tk.Canvas(canvas_frame, bg=self.colors['bg_secondary'], highlightthickness=0)
        
        # Вертикальный скроллбар
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        
        # Контейнер для заметок
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        # Привязываем обновление области прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Создаём окно на канвасе
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Настраиваем команды прокрутки
        canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Упаковываем канвас
        canvas.pack(side="left", fill="both", expand=True)
        
        # Привязываем события прокрутки для мыши (опционально)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(int(-1 * (event.delta / 120)), "units"))

        self.notes_canvas = canvas
        
    def create_settings_panel(self, parent):
        """Создание панели настроек"""
        settings_frame = tk.Frame(parent, bg=self.colors['bg_card'], height=120)
        settings_frame.pack(fill='x', side='bottom', padx=20, pady=(10, 20))
        settings_frame.pack_propagate(False)
        
        # Заголовок настроек
        tk.Label(settings_frame, text="⚙️ Настройки",
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=(10, 5))
        
        # Выбор темы
        theme_frame = tk.Frame(settings_frame, bg=self.colors['bg_card'])
        theme_frame.pack(fill='x', padx=15)
        
        tk.Label(theme_frame, text="🎨 Тема:",
                font=('Segoe UI', 9),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(side='left')
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_menu = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=list(self.themes.keys()),
                                 state='readonly', width=12)
        theme_menu.pack(side='right')
        theme_menu.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Мотивационная цитата
        self.quote_label = tk.Label(settings_frame, text="",
                                   font=('Segoe UI', 9, 'italic'),
                                   bg=self.colors['bg_card'],
                                   fg=self.colors['text_secondary'],
                                   wraplength=300)
        self.quote_label.pack(pady=(10, 5))
        
    def create_main_area(self, parent):
        """Создание основной области редактирования"""
        main_area = tk.Frame(parent, bg=self.colors['bg_primary'])
        main_area.pack(side='right', fill='both', expand=True)
        
        # Панель инструментов
        self.create_toolbar(main_area)
        
        # Область редактирования
        self.create_editor(main_area)
        
    def create_toolbar(self, parent):
        """Создание панели инструментов с улучшенными кнопками"""
        toolbar = tk.Frame(parent, bg=self.colors['bg_secondary'], height=70)
        toolbar.pack(fill='x', pady=(0, 2))
        toolbar.pack_propagate(False)
        
        # Левая группа кнопок
        left_tools = tk.Frame(toolbar, bg=self.colors['bg_secondary'])
        left_tools.pack(side='left', padx=20, pady=10)
        
        tools_data = [
            ("💾 Сохранить", self.save_notes),
            ("📁 Открыть", self.load_notes_file),
            ("❌ Удалить", self.delete_note),
            ("📄 Экспорт", self.export_note),
            ("🔄 Очистить", self.clear_editor)
        ]
        
        for text, command in tools_data:
            btn = tk.Button(left_tools,
                           text=text,
                           font=('Segoe UI', 11, 'bold'),
                           bg=self.colors['bg_card'],
                           fg=self.colors['text_primary'],
                           relief='flat',
                           bd=0,
                           cursor='hand2',
                           command=command,
                           padx=12,
                           pady=8,
                           width=10)
            # Добавляем закруглённые углы и тень через highlight
            btn.configure(highlightbackground=self.colors['border'], highlightthickness=2)
            btn.pack(side='left', padx=5)
            btn.bind('<Enter>', lambda e, b=btn: self.tool_button_hover(e, True, b))
            btn.bind('<Leave>', lambda e, b=btn: self.tool_button_hover(e, False, b))
            
        # Правая группа - информация
        right_info = tk.Frame(toolbar, bg=self.colors['bg_secondary'])
        right_info.pack(side='right', padx=20, pady=15)
        
        self.info_label = tk.Label(right_info, text="Добро пожаловать! 👋",
                                  font=('Segoe UI', 11),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_secondary'])
        self.info_label.pack()
        
        # Часы
        self.clock_label = tk.Label(right_info, text="",
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['accent'])
        self.clock_label.pack()
        self.update_clock()
        
    def create_editor(self, parent):
        """Создание области редактирования"""
        editor_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        editor_frame.pack(fill='both', expand=True, padx=25, pady=(0, 25))
        
        # Поле заголовка с плейсхолдером
        title_frame = tk.Frame(editor_frame, bg=self.colors['bg_primary'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        self.title_entry = tk.Entry(title_frame,
                                   font=('Segoe UI', 18, 'bold'),
                                   bg=self.colors['bg_card'],
                                   fg=self.colors['text_primary'],
                                   insertbackground=self.colors['text_primary'],
                                   relief='flat', bd=15)
        self.title_entry.pack(fill='x', ipady=15)
        self.title_entry.bind('<KeyRelease>', self.on_title_change)
        self.title_entry.bind('<FocusIn>', self.on_title_focus_in)
        self.title_entry.bind('<FocusOut>', self.on_title_focus_out)
        
        # Текстовое поле
        text_frame = tk.Frame(editor_frame, bg=self.colors['bg_primary'])
        text_frame.pack(fill='both', expand=True)
        
        self.text_area = tk.Text(text_frame,
                                font=('Segoe UI', 13),
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_primary'],
                                insertbackground=self.colors['text_primary'],
                                selectbackground=self.colors['accent'],
                                relief='flat', bd=20,
                                wrap='word',
                                undo=True)
        
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical",
                                      command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_area.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        self.text_area.bind('<FocusIn>', self.on_text_focus_in)
        
        # Заглушка для пустого состояния
        self.create_empty_state(editor_frame)
        
    def create_empty_state(self, parent):
        """Создание заглушки для пустого состояния"""
        self.empty_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        
        # Большая иконка
        empty_icon = tk.Label(self.empty_frame, text="📝",
                             font=('Segoe UI', 64),
                             bg=self.colors['bg_primary'],
                             fg=self.colors['text_secondary'])
        empty_icon.pack(pady=(120, 30))
        
        # Приветственный текст
        welcome_text = tk.Label(self.empty_frame,
                               text="Добро пожаловать в ZametkaAldiyara Pro!",
                               font=('Segoe UI', 20, 'bold'),
                               bg=self.colors['bg_primary'],
                               fg=self.colors['text_primary'])
        welcome_text.pack(pady=(0, 10))
        
        # Инструкция
        instruction_text = tk.Label(self.empty_frame,
                                   text="Создайте новую заметку или выберите существующую\nдля начала работы",
                                   font=('Segoe UI', 14),
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['text_secondary'],
                                   justify='center')
        instruction_text.pack(pady=(0, 30))
        
        # Горячие клавиши
        hotkeys_text = tk.Label(self.empty_frame,
                               text="💡 Горячие клавиши:\nCtrl+N - Новая заметка\nCtrl+S - Сохранить\nCtrl+F - Найти",
                               font=('Segoe UI', 11),
                               bg=self.colors['bg_primary'],
                               fg=self.colors['accent'],
                               justify='center')
        hotkeys_text.pack()
        
        self.show_empty_state()
        
    def show_empty_state(self):
        """Показать пустое состояние"""
        self.title_entry.master.pack_forget()
        self.text_area.master.pack_forget()
        self.empty_frame.pack(fill='both', expand=True)
        
    def hide_empty_state(self):
        """Скрыть пустое состояние"""
        self.empty_frame.pack_forget()
        self.title_entry.master.pack(fill='x', pady=(0, 20))
        self.text_area.master.pack(fill='both', expand=True)
        
    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        self.root.bind('<Control-n>', lambda e: self.create_new_note())
        self.root.bind('<Control-s>', lambda e: self.save_notes())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus_set())
        self.root.bind('<Control-d>', lambda e: self.delete_note())
        self.root.bind('<F5>', lambda e: self.refresh_notes_list())
        
    def change_theme(self, event=None):
        """Смена темы приложения"""
        new_theme = self.theme_var.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.colors = self.themes[new_theme]
            self.save_settings()
            self.apply_theme()
            
    def apply_theme(self):
        """Применение новой темы"""
        # Перезапуск интерфейса с новой темой
        self.root.destroy()
        self.__init__()
        
    def on_title_focus_in(self, event):
        """Обработка фокуса заголовка"""
        if self.title_entry.get() == "Введите заголовок заметки...":
            self.title_entry.delete(0, tk.END)
            self.title_entry.configure(fg=self.colors['text_primary'])
            
    def on_title_focus_out(self, event):
        """Обработка потери фокуса заголовка"""
        if not self.title_entry.get() and not self.current_note:
            self.title_entry.insert(0, "Введите заголовок заметки...")
            self.title_entry.configure(fg=self.colors['text_secondary'])
            
    def on_text_focus_in(self, event):
        """Обработка фокуса текстового поля"""
        if self.text_area.get(1.0, tk.END).strip() == "Начните писать здесь...":
            self.text_area.delete(1.0, tk.END)
            self.text_area.configure(fg=self.colors['text_primary'])
            
    def create_template_note(self):
        """Создание заметки по шаблону"""
        templates = [
            {
                'title': 'Ежедневный план',
                'content': '''📅 Дата: {date}

🎯 Цели на день:
• 
• 
• 

📝 Важные задачи:
1. 
2. 
3. 

💭 Заметки:

✅ Выполнено:
'''.format(date=datetime.now().strftime('%d.%m.%Y'))
            },
            {
                'title': 'Идея проекта',
                'content': '''💡 Название проекта: 

📋 Описание:

🎯 Цель:

🛠️ Технологии:
• 
• 

📋 Задачи:
1. 
2. 
3. 

📅 Дедлайны:

💰 Бюджет:

📝 Дополнительные заметки:
'''
            },
            {
                'title': 'Заметки встречи',
                'content': '''🤝 Встреча: 
📅 Дата: {date}
👥 Участники: 

📋 Повестка дня:
1. 
2. 
3. 

💬 Обсуждение:

✅ Решения:

📝 Следующие шаги:

📅 Следующая встреча:
'''.format(date=datetime.now().strftime('%d.%m.%Y %H:%M'))
            }
        ]
        
        # Выбор случайного шаблона
        template = random.choice(templates)
        
        note = {
            'id': len(self.notes),
            'title': template['title'],
            'content': template['content'],
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.notes.insert(0, note)
        self.refresh_notes_list()
        self.select_note(note)
        
    def open_random_note(self):
        """Открытие случайной заметки"""
        if self.notes:
            random_note = random.choice(self.notes)
            self.select_note(random_note)
        else:
            messagebox.showinfo("Информация", "Нет заметок для выбора!")
            
    def export_note(self):
        """Экспорт текущей заметки"""
        if not self.current_note:
            messagebox.showwarning("Предупреждение", "Выберите заметку для экспорта")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")],
            initialvalue=f"{self.current_note['title']}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {self.current_note['title']}\n\n")
                    f.write(f"Создано: {self.current_note['created']}\n")
                    f.write(f"Изменено: {self.current_note['modified']}\n\n")
                    f.write("---\n\n")
                    f.write(self.current_note['content'])
                messagebox.showinfo("Успех", "Заметка экспортирована!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка экспорта: {str(e)}")
                
    def clear_editor(self):
        """Очистка редактора"""
        if messagebox.askyesno("Подтверждение", "Очистить текущую заметку?"):
            self.title_entry.delete(0, tk.END)
            self.text_area.delete(1.0, tk.END)
            if self.current_note:
                self.current_note['title'] = ''
                self.current_note['content'] = ''
                self.current_note['modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.refresh_notes_list()
                
    def update_clock(self):
        """Обновление часов"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.clock_label.configure(text=f"🕒 {current_time}")
        self.root.after(1000, self.update_clock)
        
    def start_motivational_quotes(self):
        """Запуск показа мотивационных цитат"""
        quotes = [
            "Лучшее время для посадки дерева было 20 лет назад. Второе лучшее время - сейчас.",
            "Единственный способ делать отличную работу - любить то, что делаешь.",
            "Не откладывайте на завтра то, что можете сделать сегодня.",
            "Каждый день - это новая возможность стать лучше.",
            "Успех - это сумма маленьких усилий, повторяемых изо дня в день.",
            "Ваши заметки - это инвестиции в будущее себя.",
            "Записанная мысль - это сохраненная идея.",
            "Организованность - ключ к продуктивности."
        ]
        
        def update_quote():
            quote = random.choice(quotes)
            self.quote_label.configure(text=f'"{quote}"')
            # Обновление каждые 30 секунд
            self.root.after(30000, update_quote)
            
        update_quote()
        
    def button_hover(self, event, enter):
        widget = event.widget
        start_color = self.colors['accent']
        end_color = self.colors['accent_hover'] if enter else self.colors['accent']
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        steps = 10
        for step in range(steps):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / steps)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / steps)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            widget.configure(bg=color)
            self.root.update()
            time.sleep(0.02)

    def tool_button_hover(self, event, enter, btn=None):
        """Эффект наведения для кнопок инструментов"""
        widget = btn if btn else event.widget
        if enter:
            widget.configure(bg=self.colors['accent'])
        else:
            widget.configure(bg=self.colors['bg_card'])
            
    def on_search_focus_in(self, event):
        """Обработка фокуса поля поиска"""
        if self.search_entry.get() == "🔍 Найти заметку...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(fg=self.colors['text_primary'])
            
    def on_search_focus_out(self, event):
        """Обработка потери фокуса поля поиска"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "🔍 Найти заметку...")
            self.search_entry.configure(fg=self.colors['text_secondary'])
            
    def create_new_note(self):
        """Создание новой заметки"""
        note = {
            'id': len(self.notes),
            'title': 'Новая заметка',
            'content': '',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.notes.insert(0, note)
        self.refresh_notes_list()
        self.select_note(note)
        self.title_entry.focus_set()
        self.title_entry.select_range(0, tk.END)
        self.update_stats()
        
    def select_note(self, note):
        """Выбор заметки для редактирования"""
        self.current_note = note
        self.hide_empty_state()
        
        # Заполнение полей
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note['title'])
        self.title_entry.configure(fg=self.colors['text_primary'])
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, note['content'])
        self.text_area.configure(fg=self.colors['text_primary'])
        
        # Обновление информации
        self.update_info_label()
        self.refresh_notes_list()  # Обновляем список для подсветки выбранной заметки
        
    def on_title_change(self, event=None):
        """Обработка изменения заголовка"""
        if self.current_note:
            new_title = self.title_entry.get()
            if new_title != "Введите заголовок заметки...":
                self.current_note['title'] = new_title
                self.current_note['modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.refresh_notes_list()
                self.update_info_label()
            
    def on_text_change(self, event=None):
        """Обработка изменения текста"""
        if self.current_note:
            content = self.text_area.get(1.0, tk.END + '-1c')
            if content != "Начните писать здесь...":
                self.current_note['content'] = content
                self.current_note['modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.update_info_label()
                self.update_stats()
            
    def update_info_label(self):
        """Обновление информационной метки"""
        if self.current_note:
            modified = self.current_note['modified']
            content = self.current_note['content']
            word_count = len(content.split()) if content.strip() else 0
            char_count = len(content)
            
            self.info_label.configure(
                text=f" Изменено: {modified.split()[1][:5]} | "
                     f"Слов: {word_count} | Символов: {char_count}"
            )
        else:
            self.info_label.configure(text="Добро пожаловать! 👋")
            
    def update_stats(self):
        """Обновление статистики"""
        total_notes = len(self.notes)
        total_words = sum(len(note['content'].split()) for note in self.notes if note['content'].strip())
        
        self.notes_count_label.configure(text=str(total_notes))
        self.words_count_label.configure(text=str(total_words))
        
    def refresh_notes_list(self):
        """Обновление списка заметок"""
        # Очистка старых виджетов
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Отображение заметок
        for note in self.notes:
            self.create_note_card(note)
            
        self.update_stats()
            
    def create_note_card(self, note):
        """Создание карточки заметки"""
        # Определяем, выбрана ли заметка
        is_selected = self.current_note and self.current_note['id'] == note['id']
        
        card_bg = self.colors['accent'] if is_selected else self.colors['bg_card']
        text_color = self.colors['text_primary']
        
        card = tk.Frame(self.scrollable_frame,
                       bg=card_bg,
                       cursor='hand2',
                       relief='solid' if is_selected else 'flat',
                       bd=1 if is_selected else 0)
        card.pack(fill='x', pady=3, ipady=12, ipadx=18)
        
        # Заголовок заметки
        title = note['title'][:35] + "..." if len(note['title']) > 35 else note['title']
        title_label = tk.Label(card, text=f"📄 {title}",
                              font=('Segoe UI', 11, 'bold'),
                              bg=card_bg,
                              fg=text_color,
                              anchor='w')
        title_label.pack(fill='x')
        
        # Превью содержимого
        preview = note['content'][:60] + "..." if len(note['content']) > 60 else note['content']
        if preview.strip():
            preview_label = tk.Label(card, text=preview,
                                   font=('Segoe UI', 9),
                                   bg=card_bg,
                                   fg=self.colors['text_secondary'] if not is_selected else text_color,
                                   anchor='w',
                                   wraplength=280)
            preview_label.pack(fill='x', pady=(3, 0))
            
        # Нижняя информация
        info_frame = tk.Frame(card, bg=card_bg)
        info_frame.pack(fill='x', pady=(5, 0))
        
        # Дата модификации
        date_str = note['modified'].split()[1][:5]  # Только время
        date_label = tk.Label(info_frame, text=f"🕒 {date_str}",
                            font=('Segoe UI', 8),
                            bg=card_bg,
                            fg=self.colors['text_secondary'] if not is_selected else text_color,
                            anchor='w')
        date_label.pack(side='left')
        
        # Количество слов
        word_count = len(note['content'].split()) if note['content'].strip() else 0
        if word_count > 0:
            words_label = tk.Label(info_frame, text=f"📊 {word_count} слов",
                                 font=('Segoe UI', 8),
                                 bg=card_bg,
                                 fg=self.colors['text_secondary'] if not is_selected else text_color,
                                 anchor='e')
            words_label.pack(side='right')
                
        # Обработчики событий
        def select_this_note(event):
            self.select_note(note)
            
        card.bind('<Button-1>', select_this_note)
        for child in card.winfo_children():
            child.bind('<Button-1>', select_this_note)
            if hasattr(child, 'winfo_children'):
                for grandchild in child.winfo_children():
                    grandchild.bind('<Button-1>', select_this_note)
            
    def search_notes(self, *args):
        """Поиск по заметкам"""
        query = self.search_var.get().lower()
        if query == "🔍 найти заметку..." or not query:
            self.refresh_notes_list()
            return
            
        # Очистка старых результатов
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Фильтрация заметок
        filtered_notes = []
        for note in self.notes:
            if (query in note['title'].lower() or 
                query in note['content'].lower()):
                filtered_notes.append(note)
                
        # Отображение результатов
        for note in filtered_notes:
            self.create_note_card(note)
            
        # Показать количество результатов
        if not filtered_notes:
            no_results = tk.Label(self.scrollable_frame,
                                text=f"🔍 Не найдено заметок по запросу '{query}'",
                                font=('Segoe UI', 10),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_secondary'])
            no_results.pack(pady=20)
            
    def delete_note(self):
        """Удаление текущей заметки"""
        if not self.current_note:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", 
                              f"Удалить заметку '{self.current_note['title']}'?"):
            self.notes.remove(self.current_note)
            self.current_note = None
            self.refresh_notes_list()
            self.show_empty_state()
            self.update_stats()
            
    def save_notes(self):
        """Сохранение заметок в файл"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialvalue="my_notes.json"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.notes, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", f"✅ Заметки сохранены в {filename}!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ Ошибка сохранения: {str(e)}")
            
    def load_notes_file(self):
        """Загрузка заметок из файла"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    loaded_notes = json.load(f)
                    
                if messagebox.askyesno("Подтверждение", 
                                      "Заменить текущие заметки загруженными?"):
                    self.notes = loaded_notes
                else:
                    # Добавить к существующим
                    for note in loaded_notes:
                        note['id'] = len(self.notes)
                        self.notes.append(note)
                        
                self.refresh_notes_list()
                self.show_empty_state()
                messagebox.showinfo("Успех", f"✅ Заметки загружены из {filename}!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ Ошибка загрузки: {str(e)}")
            
    def load_notes(self):
        """Загрузка заметок при запуске"""
        if os.path.exists('notes_data.json'):
            try:
                with open('notes_data.json', 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
                self.refresh_notes_list()
            except:
                pass
                
    def auto_save(self):
        """Автоматическое сохранение"""
        try:
            with open('notes_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except:
            pass
            
    def start_autosave(self):
        """Запуск автосохранения"""
        def autosave_worker():
            while True:
                time.sleep(30)  # Автосохранение каждые 30 секунд
                self.auto_save()
                
        thread = threading.Thread(target=autosave_worker, daemon=True)
        thread.start()
        
    def load_settings(self):
        """Загрузка настроек"""
        try:
            if os.path.exists('app_settings.json'):
                with open('app_settings.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
        
    def save_settings(self):
        """Сохранение настроек"""
        try:
            settings = {
                'theme': self.current_theme,
                'window_position': f"{self.root.winfo_x()}+{self.root.winfo_y()}"
            }
            with open('app_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass
        
    def run(self):
        """Запуск приложения"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Установка иконки приложения (если есть)
        try:
            # Можно добавить иконку приложения
            pass
        except:
            pass
            
        self.root.mainloop()
        
    def on_closing(self):
        """Обработка закрытия приложения"""
        self.auto_save()
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    app = ModernNotesApp()
    app.run()