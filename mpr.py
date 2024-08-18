import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StudentMarksAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Marks Analysis System")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Student Marks Analysis System", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.upload_button = tk.Button(self.main_frame, text="Upload CSV File", command=self.upload_csv_file)
        self.upload_button.pack(pady=20)

        self.data = None

    def upload_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

            self.data['Total Marks'] = self.data['Physics Marks'] + self.data['Chemistry Marks'] + self.data['Maths Marks']

            self.data['Percentage'] = (self.data['Total Marks'] / 300) * 100

            self.data['Status'] = self.data['Percentage'].apply(lambda x: 'Passed' if x >= 36 else 'Failed')

            self.show_data_table()

    def show_data_table(self):
        self.main_frame.destroy()

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = list(self.data.columns)
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        for index, row in self.data.iterrows():
            self.tree.insert('', tk.END, values=row.tolist())

        self.analyze_button = tk.Button(self.table_frame, text="Analyze the Data", command=self.show_graphs)
        self.analyze_button.pack(anchor='ne', padx=20, pady=10)

    def show_graphs(self):
        self.table_frame.destroy()

        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.calculate_statistics()

        fig, axs = plt.subplots(2, 2, figsize=(12, 10))

        sns.barplot(x=['Physics', 'Chemistry', 'Maths'], y=[self.passed_physics, self.passed_chemistry, self.passed_maths], ax=axs[0, 0])
        axs[0, 0].set_title('Students Passed in Each Subject')
        axs[0, 0].set_ylabel('Number of Students')

        labels = ['Passed', 'Failed']
        sizes = [self.num_passed, self.total_students - self.num_passed]
        colors = sns.color_palette('Set2')
        axs[0, 1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        axs[0, 1].set_title('Proportion of Passed vs. Failed Students')

        sns.histplot(self.data['Percentage'], kde=True, bins=10, color='blue', ax=axs[1, 0])
        axs[1, 0].set_title('Distribution of Student Percentages')
        axs[1, 0].set_xlabel('Percentage')
        axs[1, 0].set_ylabel('Frequency')

        subjects = list(self.avg_percentages.keys())
        averages = list(self.avg_percentages.values())
        axs[1, 1].plot(subjects, averages, marker='o', color='red')
        axs[1, 1].set_title('Average Marks in Each Subject')
        axs[1, 1].set_xlabel('Subject')
        axs[1, 1].set_ylabel('Average Marks')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        self.download_button = tk.Button(self.graph_frame, text="Download Graphs as PDF", command=self.download_graphs)
        self.download_button.pack(side=tk.BOTTOM, pady=10, padx=10)

    def calculate_statistics(self):
        self.total_students = len(self.data)
        self.num_passed = len(self.data[self.data['Status'] == 'Passed'])

        pass_threshold = 36
        self.passed_physics = len(self.data[self.data['Physics Marks'] >= pass_threshold])
        self.passed_chemistry = len(self.data[self.data['Chemistry Marks'] >= pass_threshold])
        self.passed_maths = len(self.data[self.data['Maths Marks'] >= pass_threshold])

        self.avg_percentages = {
            'Physics': self.data['Physics Marks'].mean(),
            'Chemistry': self.data['Chemistry Marks'].mean(),
            'Maths': self.data['Maths Marks'].mean(),
        }

    def download_graphs(self):
        plt.savefig('student_marks_analysis_graphs.pdf')
        messagebox.showinfo("Download Complete", "Graphs have been downloaded as 'student_marks_analysis_graphs.pdf'")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = StudentMarksAnalysisApp(root)
    root.mainloop()


