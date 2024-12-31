import streamlit as st
import random
from dataclasses import dataclass
from typing import List, Optional

# Data Models
@dataclass
class Question:
    text: str
    answer: str
    solution: str
    unit: str
    topic: str
    difficulty: str

class QuizData:
    """Database of quiz questions"""
    def __init__(self):
        self.questions = {
"Hình học": {
    "Dễ": [
        Question(
            "Tính diện tích của tam giác có đáy 10cm và chiều cao 8cm.",
            "40",
            "Diện tích = (đáy × chiều cao) / 2 = (10 × 8) / 2 = 40 cm²",
            "cm²",
            "Hình học",
            "Dễ"
        ),
        Question(
            "Tính chu vi của hình chữ nhật có chiều dài 12cm và chiều rộng 7cm.",
            "38",
            "Chu vi = 2 × (dài + rộng) = 2 × (12 + 7) = 38 cm",
            "cm",
            "Hình học",
            "Dễ"
        ),
        Question(
            "Tính diện tích của một hình vuông có cạnh 9cm.",
            "81",
            "Diện tích = cạnh × cạnh = 9 × 9 = 81 cm²",
            "cm²",
            "Hình học",
            "Dễ"
        )
    ],
    "Trung bình": [
        Question(
            "Tính thể tích của hình chóp tứ giác đều có diện tích đáy 20cm² và chiều cao 9cm.",
            "60",
            "Thể tích = (1/3) × diện tích đáy × chiều cao = (1/3) × 20 × 9 = 60 cm³",
            "cm³",
            "Hình học",
            "Trung bình"
        ),
        Question(
            "Tính diện tích mặt cầu có bán kính 6cm (lấy π = 3.14).",
            "452.16",
            "Diện tích mặt cầu = 4 × π × r² = 4 × 3.14 × 6² = 452.16 cm²",
            "cm²",
            "Hình học",
            "Trung bình"
        )
    ],
    "Khó": [
        Question(
            "Một hình trụ có bán kính đáy 5cm và chiều cao 10cm. Tính diện tích xung quanh của hình trụ (lấy π = 3.14).",
            "314",
            "Diện tích xung quanh = 2 × π × r × h = 2 × 3.14 × 5 × 10 = 314 cm²",
            "cm²",
            "Hình học",
            "Khó"
        ),
        Question(
            "Một hình chóp tam giác đều có cạnh đáy 6cm và chiều cao 9cm. Tính thể tích của hình chóp đó.",
            "54",
            "Diện tích đáy = (cạnh × chiều cao đáy) / 2 = (6 × 5.2) / 2 = 15.6 cm² (giả sử chiều cao đáy là 5.2cm)\nThể tích = (1/3) × diện tích đáy × chiều cao hình chóp = (1/3) × 15.6 × 9 = 54 cm³",
            "cm³",
            "Hình học",
            "Khó"
        )
    ]
},
"Đại số": {
    "Dễ": [
        Question(
            "Giải phương trình: x + 7 = 15",
            "8",
            "x + 7 = 15\nx = 15 - 7\nx = 8",
            "",
            "Đại số",
            "Dễ"
        ),
        Question(
            "Giải phương trình: 5x = 20",
            "4",
            "5x = 20\nx = 20 / 5\nx = 4",
            "",
            "Đại số",
            "Dễ"
        )
    ],
    "Trung bình": [
        Question(
            "Giải phương trình: x² - 6x + 9 = 0",
            "x=3",
            "x² - 6x + 9 = (x - 3)² = 0\nx = 3",
            "",
            "Đại số",
            "Trung bình"
        ),
        Question(
            "Giải phương trình: x² - 7x + 12 = 0",
            "x=3;x=4",
            "x² - 7x + 12 = 0\n(x - 3)(x - 4) = 0\nx = 3 hoặc x = 4",
            "",
            "Đại số",
            "Trung bình"
        )
    ],
    "Khó": [
        Question(
            "Giải phương trình: |x - 3| + |x + 2| = 7",
            "x=0;x=5",
            "Xét các trường hợp dấu của |x - 3| và |x + 2| để giải...",
            "",
            "Đại số",
            "Khó"
        ),
        Question(
            "Giải bất phương trình: x² - x - 6 < 0",
            "-2<x<3",
            "x² - x - 6 = 0\n(x - 3)(x + 2) = 0\nNghiệm: x = 3, x = -2\nDấu biểu thức âm trong khoảng -2 < x < 3",
            "",
            "Đại số",
            "Khó"
        )
    ]
},
"Xác suất": {
    "Dễ": [
        Question(
            "Tung một xúc xắc. Tính xác suất ra số 1.",
            "1/6",
            "P(số 1) = 1/6",
            "",
            "Xác suất",
            "Dễ"
        ),
        Question(
            "Tung một đồng xu. Tính xác suất ra mặt sấp.",
            "1/2",
            "P(mặt sấp) = 1/2",
            "",
            "Xác suất",
            "Dễ"
        )
    ],
    "Trung bình": [
        Question(
            "Tung 3 đồng xu. Tính xác suất tất cả đều ngửa.",
            "1/8",
            "P(tất cả ngửa) = (1/2)³ = 1/8",
            "",
            "Xác suất",
            "Trung bình"
        ),
        Question(
            "Một túi có 4 bi đỏ và 6 bi xanh. Lấy ngẫu nhiên 2 bi. Tính xác suất cả 2 bi đều đỏ.",
            "2/15",
            "P(2 đỏ) = C(4,2)/C(10,2) = (6)/(45) = 2/15",
            "",
            "Xác suất",
            "Trung bình"
        )
    ],
    "Khó": [
        Question(
            "Một người chơi xúc xắc 3 lần. Tính xác suất ít nhất một lần ra số chẵn.",
            "7/8",
            "P(không có số chẵn) = (1/2)³ = 1/8\nP(≥1 số chẵn) = 1 - 1/8 = 7/8",
            "",
            "Xác suất",
            "Khó"
        ),
        Question(
            "Một túi có 3 bi đỏ, 2 bi xanh, và 1 bi vàng. Lấy ngẫu nhiên 3 bi. Tính xác suất lấy được đúng 1 bi đỏ.",
            "3/10",
            "P(1 đỏ) = C(3,1)×C(3,2)/C(6,3) = (3×3)/(20) = 3/10",
            "",
            "Xác suất",
            "Khó"
        )
    ]
}
        }

class QuizManager:
    """Manages quiz generation and scoring"""
    def __init__(self, data: QuizData):
        self.data = data

    def get_available_questions(self, topics: List[str], difficulties: List[str]) -> List[Question]:
        """Get all questions matching the selected topics and difficulties"""
        questions = []
        for topic in topics:
            for diff in difficulties:
                if topic in self.data.questions and diff in self.data.questions[topic]:
                    questions.extend(self.data.questions[topic][diff])
        return questions

    def generate_quiz(self, topics: List[str], difficulties: List[str], num_questions: int = 5) -> List[Question]:
        """Generate a quiz with the specified number of questions"""
        available = self.get_available_questions(topics, difficulties)
        if len(available) < num_questions:
            return []
        return random.sample(available, num_questions)

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Check if the user's answer is correct"""
        user_answer = user_answer.replace(" ", "").lower()
        correct_answer = str(correct_answer).replace(" ", "").lower()
        return user_answer == correct_answer

    def calculate_score(self, questions: List[Question], answers: List[str]) -> float:
        """Calculate the score for the quiz"""
        if not questions:
            return 0.0
        correct = sum(self.check_answer(user_ans, q.answer) for user_ans, q in zip(answers, questions))
        return (correct / len(questions)) * 10

class QuizApp:
    """Main quiz application"""
    def __init__(self):
        self.quiz_data = QuizData()
        self.quiz_manager = QuizManager(self.quiz_data)
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize or reset session state"""
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'answers' not in st.session_state:
            st.session_state.answers = []
        if 'submitted' not in st.session_state:
            st.session_state.submitted = False

    def render_sidebar(self) -> tuple[List[str], List[str]]:
        """Render the sidebar with quiz options"""
        st.sidebar.header("Tùy chọn đề kiểm tra")
        
        topics = st.sidebar.multiselect(
            "Chọn chủ đề:",
            ["Hình học", "Đại số", "Xác suất"],
            default=["Hình học"]
        )
        
        difficulties = st.sidebar.multiselect(
            "Chọn độ khó:",
            ["Dễ", "Trung bình", "Khó"],
            default=["Dễ"]
        )

        if st.sidebar.button("Tạo đề kiểm tra mới"):
            if not topics or not difficulties:
                st.error("Vui lòng chọn ít nhất một chủ đề và một độ khó!")
                return topics, difficulties

            questions = self.quiz_manager.generate_quiz(topics, difficulties)
            if not questions:
                st.error("Không đủ câu hỏi với các tiêu chí đã chọn. Vui lòng chọn thêm chủ đề hoặc độ khó!")
                return topics, difficulties

            st.session_state.questions = questions
            st.session_state.answers = [''] * len(questions)
            st.session_state.submitted = False

        return topics, difficulties

    def render_quiz(self):
        """Render the quiz questions"""
        if not st.session_state.questions:
            return

        st.subheader("Bài kiểm tra của bạn:")
        
        if len(st.session_state.answers) != len(st.session_state.questions):
            st.session_state.answers = [''] * len(st.session_state.questions)
        
        for i, question in enumerate(st.session_state.questions):
            st.write(f"**Câu {i+1}:** {question.text}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.session_state.answers[i] = st.text_input(
                    f"Nhập câu trả lời {i+1}",
                    value=st.session_state.answers[i],
                    key=f"answer_{i}"
                )
            with col2:
                if question.unit:
                    st.write(f"Đơn vị: {question.unit}")

        if st.button("Nộp bài"):
            st.session_state.submitted = True

    def render_results(self):
        """Render the quiz results"""
        if not st.session_state.submitted:
            return

        score = self.quiz_manager.calculate_score(
            st.session_state.questions, 
            st.session_state.answers
        )

        st.markdown("---")
        st.subheader("Kết quả kiểm tra:")
        st.write(f"**Điểm số của bạn: {score:.2f}/10**")
        
        st.write("### Chi tiết bài làm:")
        for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
            with st.expander(f"Câu {i+1}"):
                st.write(f"**Câu hỏi:** {question.text}")
                st.write(f"**Câu trả lời của bạn:** {answer} {question.unit}")
                st.write(f"**Đáp án đúng:** {question.answer} {question.unit}")
                
                is_correct = self.quiz_manager.check_answer(answer, question.answer)
                if is_correct:
                    st.success("✓ Đúng")
                else:
                    st.error("✗ Sai")
                
                st.write("**Lời giải:**")
                st.write(question.solution)

    def render_statistics(self, topics: List[str], difficulties: List[str]):
        """Render statistics in the sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("Thống kê:")
        
        total = len(self.quiz_manager.get_available_questions(topics, difficulties))
        st.sidebar.write(f"Tổng số câu hỏi có sẵn: {total}")
        
        for topic in topics:
            for diff in difficulties:
                if topic in self.quiz_data.questions and diff in self.quiz_data.questions[topic]:
                    count = len(self.quiz_data.questions[topic][diff])
                    st.sidebar.write(f"{topic} - {diff}: {count} câu")

    def run(self):
        """Run the quiz application"""
        st.title("Hệ thống tạo và chấm điểm bài kiểm tra Toán")
        
        topics, difficulties = self.render_sidebar()
        if topics and difficulties:
            self.render_statistics(topics, difficulties)
        
        self.render_quiz()
        self.render_results()

if __name__ == "__main__":
    app = QuizApp()
    app.run()