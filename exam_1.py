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
                        "Tính diện tích hình chữ nhật có chiều dài 6cm và chiều rộng 4cm.",
                        "24",
                        "Diện tích = dài × rộng = 6 × 4 = 24 cm²",
                        "cm²",
                        "Hình học",
                        "Dễ"
                    ),
                    Question(
                        "Tính chu vi của một hình vuông có cạnh 5cm.",
                        "20",
                        "Chu vi = 4 × cạnh = 4 × 5 = 20 cm",
                        "cm",
                        "Hình học",
                        "Dễ"
                    )
                ],
                "Trung bình": [
                    Question(
                        "Tính diện tích hình thang có đáy lớn 10cm, đáy nhỏ 6cm và chiều cao 4cm.",
                        "32",
                        "Diện tích = ((đáy lớn + đáy nhỏ) × chiều cao)/2 = ((10 + 6) × 4)/2 = 32 cm²",
                        "cm²",
                        "Hình học",
                        "Trung bình"
                    )
                ],
                "Khó": [
                    Question(
                        "Một hình lập phương có thể tích 216cm³. Tính diện tích xung quanh của hình lập phương đó.",
                        "216",
                        "Cạnh = ∛216 = 6cm\nDiện tích xung quanh = 4 × cạnh² = 4 × 6² = 216 cm²",
                        "cm²",
                        "Hình học",
                        "Khó"
                    )
                ]
            },
            "Đại số": {
                "Dễ": [
                    Question(
                        "Giải phương trình: 2x + 5 = 13",
                        "4",
                        "2x + 5 = 13\n2x = 8\nx = 4",
                        "",
                        "Đại số",
                        "Dễ"
                    )
                ],
                "Trung bình": [
                    Question(
                        "Giải hệ phương trình:\nx + y = 5\n2x - y = 1",
                        "x=2,y=3",
                        "Từ pt 1: y = 5 - x\nThay vào pt 2: 2x - (5-x) = 1\n3x = 6\nx = 2\ny = 5 - 2 = 3",
                        "",
                        "Đại số",
                        "Trung bình"
                    )
                ],
                "Khó": [
                    Question(
                        "Giải phương trình: |2x - 1| + |x + 2| = 5",
                        "x=-3;x=2",
                        "Xét các trường hợp dấu của |2x - 1| và |x + 2|...",
                        "",
                        "Đại số",
                        "Khó"
                    )
                ]
            },
            "Xác suất": {
                "Dễ": [
                    Question(
                        "Tung một đồng xu cân đối 2 lần. Tính xác suất được ít nhất 1 mặt ngửa.",
                        "3/4",
                        "P(ít nhất 1 mặt ngửa) = 1 - P(không có mặt ngửa) = 1 - 1/4 = 3/4",
                        "",
                        "Xác suất",
                        "Dễ"
                    )
                ],
                "Trung bình": [
                    Question(
                        "Tung 3 đồng xu cân đối. Tính xác suất được đúng 2 mặt ngửa.",
                        "3/8",
                        "P(2 mặt ngửa) = C(3,2)×(1/2)³ = 3/8",
                        "",
                        "Xác suất",
                        "Trung bình"
                    )
                ],
                "Khó": [
                    Question(
                        "Một xạ thủ bắn 3 phát với xác suất trúng đích mỗi phát là 0.8. Tính xác suất có ít nhất 2 phát trúng đích.",
                        "0.896",
                        "P(≥2 trúng) = C(3,2)×0.8²×0.2 + C(3,3)×0.8³ = 0.896",
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