import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import os
import glob

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz de Perguntas - Comercial Alvorada")

        # Pergunta o nome do usuário
        self.user_name = simpledialog.askstring("Nome do Usuário", "Por favor, insira seu nome:")
        if not self.user_name:
            self.user_name = "Usuario"  # Nome padrão se nada for inserido

        self.questions = [
            {"question": "1. CERA CARNAÚBA HYBRID OFERECE PROTEÇÃO CONTRA RAIOS UV?", "options": ["Verdadeiro", "Falso"], "answer": "Verdadeiro"},
            {"question": "3. O PNEU PRETINHO VINTEX NÃO OFERECE PROTEÇÃO CONTRA OS RAIOS UV?", "options": ["Verdadeiro", "Falso"], "answer": "Falso"},
            {"question": "4. QUAL PRODUTO MAIS INDICADO PARA REMOVER MANCHAS DE ÁGUA OU CALCIFICAÇÃO NOS VIDROS?", "options": ["PRIZM", "VIDREXX MAX","GLAZY","VIBREXX"], "answer": "PRIZM"},
            {"question": "5. QUAL PRODUTO É IDEAL PARA LIMPEZA DE MOTOS?", "options": ["MOTO-V", "V-MOL"], "answer": "MOTO-V"},
            {"question": "6. PARA REMOÇÃO DE PICHE E COLA INDICAMOS DELET.", "options": ["VERDADEIRO", "FALSO"], "answer": "Falso"},
            {"question": "7. HIGICOURO PODE SER UTILIZADO APENAS NA LIMPEZA DE COURO NATURAL, E NÃO PODE SER APLICADO EM COURO SINTÉTICO.", "options": ["VERDADEIRO", "FALSO"], "answer": "FALSO"},
            {"question": "8. RESTAURAX RENOVA E RESTAURA SUPERFÍCIES PLÁSTICAS, COMO PARA-CHOQUES, PAINÉIS E LATERAIS DE PORTAS.", "options": ["VERDADEIRO", "FALSO"], "answer": "Verdadeiro"},
            {"question": "9. QUAL DESSES PRODUTOS RECUPERA FARÓES QUE SOFRERAM OXIDAÇÃO COM O PASSAR DO TEMPO?", "options": ["V-LIGHT", "NATIVE","HIBRID WAX","GLADIUS"], "answer": "V-LIGHT"},
            {"question": "10. ALUMAX É UM DESENCRUSTANTE ÁCIDO PARA LIMPEZA DE GRAXAS E REMOÇÃO DE BARROS.", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "11. SINTRA PRO É UM LIMPADOR BACTERICIDA?", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "12. V-ECO VONIXX É A LINHA ECOLÓGICA QUE LAVA A SECO", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "13. MARQUE A ALTERNATIVA QUE TENHA SOMENTE LAVA AUTOS.", "options": ["CITRON, V-FLOC, V-MOL", "CITRON, V-FLOC, MOTO-V", "CITRON, SINTRA, MOTO-V", "CITRON, V-LUB, MOTO-V"], "answer": "CITRON, V-FLOC, V-MOL"},
            {"question": "14. O PRODUTO DELET É UM LIMPADOR DE PNEUS E BORRACHAS?", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "15. O PRODUTO IZER É UM DESCONTAMINANTE FERROSO, NÃO RETIRA FERRUGEM.", "options": ["VERDADEIRO", "FALSO"], "answer": "FALSO"}       
        ]

        self.score = 0
        self.question_index = 0
        self.start_time = None
        self.response_time = []
        self.user_results = []  # Lista para armazenar resultados do usuário
        self.time_limit = 40  # Tempo limite em segundos
        self.timer_update_id = None
        self.timer_label = tk.Label(self.master, text="")
        self.timer_label.pack()

        self.question_label = tk.Label(self.master, text="")
        self.question_label.pack()

        self.options_var = tk.StringVar()
        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack()

        self.options = []
        self.create_options()
        self.next_question()

    def create_options(self):
        for i in range(4):
            option = tk.Radiobutton(self.options_frame, text="", variable=self.options_var, value="")
            option.pack(anchor="w")
            self.options.append(option)

        self.submit_button = tk.Button(self.options_frame, text="Enviar", command=self.submit_answer)
        self.submit_button.pack(pady=10)

    def next_question(self):
        if self.question_index < len(self.questions):
            self.stop_timer()
            self.start_time = time.time()
            self.update_timer(self.time_limit)
            question = self.questions[self.question_index]
            self.question_label.config(text=question["question"])

            for i, option in enumerate(self.options):
                if i < len(question["options"]):
                    option.config(text=question["options"][i], value=question["options"][i])
                    option.pack()
                else:
                    option.pack_forget()

            self.options_var.set(question["options"][0])
        else:
            self.show_results()

    def stop_timer(self):
        self.timer_label.config(text="")
        if self.timer_update_id:
            self.master.after_cancel(self.timer_update_id)

    def update_timer(self, remaining_time):
        self.timer_label.config(text=f"Tempo restante: {remaining_time} segundos")
        if remaining_time > 0:
            self.timer_update_id = self.master.after(1000, self.update_timer, remaining_time - 1)
        else:
            messagebox.showinfo("Tempo Esgotado", "O tempo para responder acabou!")
            self.submit_answer()

    def submit_answer(self):
        if self.question_index < len(self.questions):
            end_time = time.time()
            time_taken = end_time - self.start_time
            answer = self.options_var.get()
            correct_answer = self.questions[self.question_index]["answer"]

            if answer == correct_answer:
                self.score += 1
                messagebox.showinfo("Resultado", "Você acertou!")
            else:
                messagebox.showinfo("Resultado", "Você errou!")

            self.response_time.append({
                "question": self.questions[self.question_index]["question"],
                "time_taken": time_taken,
                "correct": answer == correct_answer
            })

            self.question_index += 1
            self.next_question()

    def show_results(self):
        results = f"Você acertou {self.score} de {len(self.questions)} perguntas.\n\n"
        results += "Detalhes das Respostas:\n"
        for response in self.response_time:
            results += f"{response['question']} - Tempo: {response['time_taken']:.2f}s - {'Correto' if response['correct'] else 'Incorreto'}\n"

        # Salvar os resultados em um arquivo TXT com o nome do usuário
        file_name = f"{self.user_name}_resultados_quiz.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(results)

        # Exibe os resultados na tela
        messagebox.showinfo("Resultados", f"Resultados salvos em: {os.path.abspath(file_name)}\n\n{results}")

        # Atualiza o ranking
        self.update_ranking()

    def update_ranking(self):
        all_results = []

        # Lê todos os arquivos .txt de resultados
        for file_path in glob.glob("*_resultados_quiz.txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    # A última linha contém os detalhes da pontuação
                    score_line = lines[0]  # A primeira linha deve conter o resultado
                    score = int(score_line.split(" ")[2])  # "Você acertou X de Y perguntas."
                    username = file_path.split("_")[0]  # Extrai o nome do usuário do nome do arquivo

                    # Recupera o tempo total do arquivo de resultados
                    total_time = self.calculate_total_time(file_path)

                    # Adiciona o resultado e o tempo total do quiz
                    all_results.append((username, score, total_time))

        # Ordena o ranking com base na pontuação e no tempo total
        all_results.sort(key=lambda x: (-x[1], x[2]))

        ranking = "Ranking:\n"
        for i, (username, score, total_time) in enumerate(all_results):
            ranking += f"{i + 1}. {username} - {score} pontos - Tempo total: {total_time:.2f}s\n"

        # Salva o ranking em um arquivo
        with open("ranking.txt", "w", encoding="utf-8") as file:
            file.write(ranking)

        messagebox.showinfo("Ranking", ranking)

    def calculate_total_time(self, file_path):
        total_time = 0.0
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines[1:]:  # Ignora a primeira linha com a contagem de acertos
                if "Tempo" in line:  # Verifica se a linha contém detalhes do tempo
                    parts = line.split(" - ")
                    time_part = parts[1]  # "Tempo: X.XXs"
                    time_value = float(time_part.split(": ")[1][:-1])  # Extrai o valor do tempo
                    total_time += time_value
        return total_time

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
