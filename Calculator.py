import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random


# st.set_page_config(layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "About Calculator", "Contact Us", "Gift"],
    icons=["house", "projector", "envelope", "gift"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    def plot_custom_functions(user_inputs, show_grid, show_legend, show_axis_labels):
        x = np.linspace(-10, 10, 1000)

        fig, ax = plt.subplots()

        for user_input in user_inputs:
            try:
                expr = sp.sympify(user_input)
                func = sp.lambdify('x', expr, 'numpy')
                y = func(x)

                ax.plot(x, y, label=user_input)
                
            except Exception as e:
                st.sidebar.error(f"Error: {e}. Please enter a valid mathematical expression for '{user_input}'.")
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            

        if show_grid:
            ax.grid(True, which='both', linestyle='--', linewidth=0.5)

            ax.xaxis.set_major_locator(plt.MultipleLocator(1))
            ax.yaxis.set_major_locator(plt.MultipleLocator(1))

            ax.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
            ax.yaxis.set_minor_locator(plt.MultipleLocator(0.5))

        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])

        if show_legend:
           ax.legend()

        if show_axis_labels:
           ax.set_xlabel('x')
           ax.set_ylabel('y')

        ax.set_title('Functions')
        st.pyplot(fig)


    def main():
        st.title('Trignometric Function Graphs Calculator')
        st.sidebar.subheader('🛠️ Function Inputs')
        num_functions = st.sidebar.number_input("Enter the number of functions:", min_value=1, max_value=10, value=1)
    
        user_inputs = []
        for i in range(num_functions):
            user_input = st.sidebar.text_input(f"Function {i + 1}", value="sin(x)")
            user_inputs.append(user_input)

        st.sidebar.subheader('Settings')

        show_grid = st.sidebar.checkbox("Show Grid", value=True)
        show_legend = st.sidebar.checkbox("Show Legend", value=True)
        show_axis_labels = st.sidebar.checkbox("Show Axis Labels", value=True)
        
        plot_custom_functions(user_inputs, show_grid, show_legend, show_axis_labels)


    if __name__ == "__main__":
        main()


elif selected == "About Calculator":
    st.subheader("🎈 :red[Purpose]")
    st.write("The Trignometric Graphic Calculator is a powerful tool designed to help users visualize and explore mathematical functions with ease. Whether you are a student, educator, or anyone passionate about mathematics, this calculator serves as an invaluable resource for understanding and experimenting with various functions.")

    st.subheader("⛏️ :red[Functionality]")
    st.write("The calculator boasts a user-friendly interface that empowers users to input mathematical expressions effortlessly. Leveraging the capabilities of Python libraries like NumPy, Matplotlib, and SymPy, it instantaneously generates graphical representations of the input functions. This creates a seamless and interactive environment, allowing users to explore mathematical concepts dynamically.")

    st.subheader("🔑 :red[Key Features]")
    st.write("1. 👉 :blue[Custom Feature]")
    st.write("Users can input multiple mathematical expressions simultaneously, enabling the exploration of a wide spectrum of functions, from the fundamental to the intricate.")
    st.write("2. 👉 :blue[Graphical Visualization]")
    st.write("The calculator facilitates dynamic plotting of functions in real-time. Additionally, users can leverage zoom and pan features for a closer examination of the generated graphs.")
    st.write("3. 👉 :blue[User-Friendly Interface]")
    st.write("With a simple and intuitive sidebar, users can efficiently manage input and settings. Customization options, including grid display, legend visibility, and axis label preferences, enhance the overall user experience.")
    st.write("4. 👉 :blue[Error Handling]")
    st.write("The calculator ensures a smooth user experience by providing informative error messages in cases of invalid expressions. This feature contributes to a frustration-free exploration of mathematical functions.")
    st.write("5. 👉 :blue[Advance Functions]")
    st.write("The calculator supports a diverse range of advanced mathematical functions. From trigonometric and exponential functions to logarithmic expressions, users can harness the power of SymPy for symbolic computation. This capability enables the exploration of complex algebraic expressions.")
    st.subheader("🚀 :red[Limitations]")
    st.write("1. The calculator may struggle with extremely complex or computationally intensive functions. While it handles a wide range of expressions, there might be cases where performance is impacted.")
    st.write("2. The calculator generates graphs based on user inputs, but it doesn't provide real-time updates. Users need to manually input changes to see updated graphs.")
    st.write("3. While the calculator supports a variety of functions, its capabilities for handling multivariable functions, especially in 3D graphing, may be limited")


elif selected == "Contact Us":
    st.title("Contact Us")

    st.write(
        "How Can We Help You Plz Contact Us and We Will Respond As Soon as Possible"
    )

    name = st.text_input("🧑 Name:")
    email = st.text_input("✉️ Email:")
    message = st.text_area("💬 Message:", height=150)

    if st.button("📤 Submit"):
        st.success("Your message has been submitted. We'll be in touch soon!")

elif selected == "Gift":

    def init(post_init=False):
        if not post_init:
            st.session_state.opponent = 'Human'
            st.session_state.win = {'X': 0, 'O': 0}
        st.session_state.board = np.full((3, 3), '.', dtype=str)
        st.session_state.player = 'X'
        st.session_state.warning = False
        st.session_state.winner = None
        st.session_state.over = False


    def check_available_moves(extra=False) -> list:
        raw_moves = [row for col in st.session_state.board.tolist() for row in col]
        num_moves = [i for i, spot in enumerate(raw_moves) if spot == '.']
        if extra:
            return [(i // 3, i % 3) for i in num_moves]
        return num_moves


    def check_rows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return None


    def check_diagonals(board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return None


    def check_state():
        if st.session_state.winner:
            st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")
        if st.session_state.warning and not st.session_state.over:
            st.warning('⚠️ This move already exist')
        if st.session_state.winner and not st.session_state.over:
            st.session_state.over = True
            st.session_state.win[st.session_state.winner] = (
                st.session_state.win.get(st.session_state.winner, 0) + 1
            )
        elif not check_available_moves() and not st.session_state.winner:
            st.info(f'It\'s a tie 📍')
            st.session_state.over = True


    def check_win(board):
        for new_board in [board, np.transpose(board)]:
            result = check_rows(new_board)
            if result:
                return result
        return check_diagonals(board)


    def computer_player():
        moves = check_available_moves(extra=True)
        if moves:
            i, j = random.choice(moves)
            handle_click(i, j)


    def handle_click(i, j):
        if (i, j) not in check_available_moves(extra=True):
            st.session_state.warning = True
        elif not st.session_state.winner:
            st.session_state.warning = False
            st.session_state.board[i, j] = st.session_state.player
            st.session_state.player = "O" if st.session_state.player == "X" else "X"
            winner = check_win(st.session_state.board)
            if winner != ".":
               st.session_state.winner = winner

    def main():
        st.write(
            """
            # Gift For You
            """
        )
        
        if "board" not in st.session_state:
            init()
            
        reset, score, player, settings = st.columns([0.5, 0.6, 1, 1])
        reset.button('New game', on_click=init, args=(True,))

        with settings.expander('Settings'):
            st.write('**Warning**: changing this setting will restart your game')
            st.selectbox(
                'Set opponent',
                ['Human', 'Computer'],
                key='opponent',
                on_change=init,
                args=(True,),
            )

        for i, row in enumerate(st.session_state.board):
             cols = st.columns([5, 1, 1, 1, 5])
             for j, field in enumerate(row):
                 cols[j + 1].button(
                     field,
                     key=f"{i}-{j}",
                     on_click=handle_click
                     if st.session_state.player == 'X'
                     or st.session_state.opponent == 'Human'
                     else computer_player(),
                     args=(i, j),
                 )

        check_state()

        score.button(f'❌{st.session_state.win["X"]} 🆚 {st.session_state.win["O"]}⭕')
        player.button(
            f'{"❌" if st.session_state.player == "X" else "⭕"}\'s turn'
            if not st.session_state.winner
            else f'🏁 Game finished'
        )


    if __name__ == '__main__':
        main()
