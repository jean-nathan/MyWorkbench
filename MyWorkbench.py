import mysql.connector
import pandas as pd
from tkinter import Tk, ttk, StringVar, messagebox, filedialog, Text, Label, DISABLED, NORMAL, OptionMenu
import configparser
import threading
import time
import os

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta e Salvamento")
        
        # Initialize variables
        self.mydb = None
        self.mycursor = None
        self.column_names = []
        self.result_data = None
        self.fetch_status_label = None
        self.fetch_start_time = None
        self.connected = False  # Track connection status

        # Load login data from config
        self.config_file = 'database_config.ini'
        self.config = configparser.ConfigParser()

        # Ensure config file exists with default values if not already present
        self.create_config_file()

        # Set up notebook interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Connection configuration tab
        self.connection_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.connection_tab, text='Configurar Conexão')
        self.setup_connection_tab()

        # Query execution tab
        self.query_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.query_tab, text='Consultar Dados')
        self.setup_query_tab()

    def create_config_file(self):
        # Check if config file exists; if not, create with default values
        if not os.path.exists(self.config_file):
            self.config['Login'] = {
                'host': '',
                'user': '',
                'password': ''
            }
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)

    def save_login_data(self):
        # Save login data to config file if checkbox is checked
        if self.save_login_var.get() == '1':
            self.config['Login'] = {
                'host': self.host_var.get(),
                'user': self.user_var.get(),
                'password': self.password_var.get()
            }
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)

    def load_login_data(self):
        # Load saved login data from config file
        try:
            self.config.read(self.config_file)
            self.host_var.set(self.config.get('Login', 'host'))
            self.user_var.set(self.config.get('Login', 'user'))
            self.password_var.set(self.config.get('Login', 'password'))
            self.save_login_var.set('1')  # Check the checkbox if data is loaded
        except (configparser.Error, configparser.NoSectionError, configparser.NoOptionError):
            self.save_login_var.set('0')  # Uncheck the checkbox if data is not found

    def setup_connection_tab(self):
        # Components of connection configuration tab
        ttk.Label(self.connection_tab, text="Host:").grid(row=0, column=0, padx=10, pady=10)
        self.host_var = StringVar()
        self.host_entry = ttk.Entry(self.connection_tab, textvariable=self.host_var, width=30)
        self.host_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.connection_tab, text="Usuário:").grid(row=1, column=0, padx=10, pady=10)
        self.user_var = StringVar()
        self.user_entry = ttk.Entry(self.connection_tab, textvariable=self.user_var, width=30)
        self.user_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.connection_tab, text="Senha:").grid(row=2, column=0, padx=10, pady=10)
        self.password_var = StringVar()
        self.password_entry = ttk.Entry(self.connection_tab, textvariable=self.password_var, width=30, show='*')
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.show_password_button = ttk.Button(self.connection_tab, text="👁️", width=3, command=self.toggle_password_visibility)
        self.show_password_button.grid(row=2, column=2, padx=10, pady=10)

        self.save_login_var = StringVar(value='0')
        self.save_login_checkbox = ttk.Checkbutton(self.connection_tab, text="Salvar dados de conexão", variable=self.save_login_var)
        self.save_login_checkbox.grid(row=3, column=0, columnspan=2, pady=10)

        connect_frame = ttk.Frame(self.connection_tab)
        connect_frame.grid(row=4, column=0, columnspan=3, pady=20)

        self.connect_button = ttk.Button(connect_frame, text="Conectar ao Banco de Dados", command=self.connect_to_database)
        self.connect_button.pack(side='left', padx=5)

        self.disconnect_button = ttk.Button(connect_frame, text="Desconectar", state=DISABLED, command=self.disconnect_from_database)
        self.disconnect_button.pack(side='left', padx=5)

        # Load login data if available
        self.load_login_data()

    def toggle_password_visibility(self):
        # Toggle password visibility
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')

    def connect_to_database(self):
        # Get user input for database connection
        host = self.host_var.get()
        user = self.user_var.get()
        password = self.password_var.get()
        
        # Validate required fields
        if not host or not user or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Try to connect to database
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                ssl_disabled=True
            )
            self.mycursor = self.mydb.cursor()
            messagebox.showinfo("Conectado", "Conexão bem-sucedida ao banco de dados.")
            self.connected = True  # Set connection status
            self.disconnect_button.config(state=NORMAL)  # Enable disconnect button
            self.connect_button.config(state=DISABLED)   # Disable connect button
            # Save login data if checkbox is checked
            self.save_login_data()
        except mysql.connector.Error as error:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {error}")

    def disconnect_from_database(self):
        # Disconnect from the database
        if self.mydb:
            self.mydb.close()
            self.mydb = None
            self.mycursor = None
            self.connected = False  # Reset connection status
            self.disconnect_button.config(state=DISABLED)  # Disable disconnect button
            self.connect_button.config(state=NORMAL)       # Enable connect button
            messagebox.showinfo("Desconectado", "Desconexão bem-sucedida do banco de dados.")

    def setup_query_tab(self):
        # Components of query tab
        self.query_input = Text(self.query_tab, width=50, height=10)
        self.query_input.pack(pady=10)

        # Frame to hold query buttons
        button_frame = ttk.Frame(self.query_tab)
        button_frame.pack(pady=10)

        self.query_button = ttk.Button(button_frame, text="Executar Consulta", command=self.execute_query)
        self.query_button.pack(side='left', padx=5)

        save_options = ["Salvar como CSV", "Salvar como XLSX", "Salvar como INSERT"]
        self.save_option = StringVar()
        self.save_option.set(save_options[0])  # Default selection
        save_menu = OptionMenu(button_frame, self.save_option, *save_options)
        save_menu.pack(side='left', padx=5)

        self.save_button = ttk.Button(button_frame, text="Salvar Resultados", command=self.save_results)
        self.save_button.pack(side='left', padx=5)
        
        # Text widget to display last record print
        self.last_record_text = Text(self.query_tab, width=50, height=10, wrap='word')  # Allow word wrap for vertical expansion
        self.last_record_text.pack(pady=10, fill='both', expand=True)

        # Make the last record text widget read-only
        self.last_record_text.config(state='disabled')

        # Label for showing fetching status and time
        self.fetch_status_label = Label(self.query_tab, text="", anchor='se', fg='white')  # Set text color to white
        self.fetch_status_label.pack(side='right', padx=10, pady=10)

    def toggle_widgets_state(self, state):
        # Toggle state of widgets
        widgets_to_toggle = [
            self.host_entry,
            self.user_entry,
            self.password_entry,
            self.show_password_button,
            self.save_login_checkbox,
            self.connect_button,
            self.disconnect_button,
            self.query_input,
            self.query_button,
            self.save_button
        ]

        for widget in widgets_to_toggle:
            widget.config(state=state)

    def execute_query(self):
        # Check if database connection is established
        if not self.connected:
            messagebox.showerror("Erro", "Nenhuma conexão com o banco de dados. Conecte-se primeiro.")
            return

        # Disable widgets during query execution
        self.toggle_widgets_state(DISABLED)

        # Get SQL query from the input widget
        sql_query = self.query_input.get("1.0", "end-1c")

        # Update status label to show fetching message and start time
        self.fetch_status_label.config(text="Buscando dados...")
        self.fetch_start_time = time.time()

        # Execute SQL query in a separate thread
        threading.Thread(target=self.execute_query_thread, args=(sql_query,)).start()

    def execute_query_thread(self, sql_query):
        try:
            # Execute SQL query
            self.mycursor.execute(sql_query)
            self.column_names = [col[0] for col in self.mycursor.description]
            self.result_data = self.mycursor.fetchall()

            total_records = len(self.result_data)
            elapsed_time = round(time.time() - self.fetch_start_time, 2)

            # Update status label to show completion message and elapsed time
            self.fetch_status_label.config(text=f"Concluído. Registros: {total_records}. Tempo: {elapsed_time}s", fg="green")
            
            # Display last record print in the Text widget
            if total_records > 0:
                last_record = self.result_data[-1]
                self.last_record_text.config(state=NORMAL)  # Enable text widget for insert
                self.last_record_text.delete('1.0', 'end')  # Clear previous content
                self.last_record_text.insert('end', "\nÚltimo registro:\n")
                for col_name, value in zip(self.column_names, last_record):
                    print_text = f"{col_name}: {value}\n"
                    self.last_record_text.insert('end', print_text)
                self.last_record_text.config(state='disabled')  # Disable text widget after insert

            messagebox.showinfo("Consulta Concluída", f"Total de registros encontrados: {total_records}")
        except mysql.connector.Error as error:
            self.fetch_status_label.config(text="Erro ao buscar dados", fg="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao executar a consulta: {error}")
        finally:
            # Enable widgets after query execution
            self.toggle_widgets_state(NORMAL)

    def save_results(self):
        # Check if there are results to save
        if not self.result_data:
            messagebox.showwarning("Sem Dados", "Nenhum dado para salvar.")
            return

        save_option = self.save_option.get()

        # Request file location and format
        filetypes = [("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("SQL Files", "*.sql")]
        defaultextension = ".csv" if save_option in ["Salvar como CSV", "Salvar como XLSX"] else ".sql"
        filename = filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)
        if not filename:
            messagebox.showwarning("Nenhum arquivo selecionado", "Nenhum arquivo selecionado para salvar.")
            return
        
        try:
            if save_option == "Salvar como CSV":
                df = pd.DataFrame(self.result_data, columns=self.column_names)
                df.to_csv(filename, index=False)
            elif save_option == "Salvar como XLSX":
                df = pd.DataFrame(self.result_data, columns=self.column_names)
                df.to_excel(filename, index=False)
            elif save_option == "Salvar como INSERT":
                with open(filename, 'w') as f:
                    table_name = "<table_name>"  # Replace with your actual table name
                    columns = ', '.join(self.column_names)
                    for record in self.result_data:
                        values = ', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in record)
                        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"
                        f.write(sql_insert)

            messagebox.showinfo("Salvo!", f"Dados salvos em '{filename}'.")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar os dados: {e}")

# Main block
if __name__ == "__main__":
    root = Tk()
    app = DatabaseApp(root)
    root.mainloop()