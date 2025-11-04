import streamlit as st
from game_logic import initialize_board,check_winner
from llm_agent import setup_gemini,gemini_move,load_local_model,local_llm_move
import time
def render_board(board):
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            symbol = board[idx] if board[idx] != " " else "⬜️"
            cols[col].markdown(f"<h2 style='text-align:center'>{symbol}</h2>", unsafe_allow_html=True)
def main():
    print("Battle!!!!!!!!!!!")
    
    st.set_page_config(page_title="Battle of LLMs: Tic-Tac_Toe",layout="wide")
    st.title("🤖 Battle of LLMs: Tic-Tac-Toe")
    gemini_api = st.text_input("Enter your Gemini API Key:",type="password")
    first_player = st.selectbox("Select First Player:",["Gemini","Local_LLM]"])
    model,tokenizer,device = load_local_model()
    if st.button("Start Battle") and gemini_api:
        
        time.sleep(10)
        gemini_client  = setup_gemini(gemini_api)
        
        score = {"Gemini":0,"Local_LLM":0}
        for match in range(1,2):
            board = initialize_board()
            render_board(board)
            
            turn = 1 if first_player == "Gemini" else 2
            winner = None
            st.write("f Match {match}")
            j = 1
            while True:
                if turn == 1:
                    symbol = "X"
                    move = gemini_move(board,symbol,gemini_client)
                    board[move] = symbol
                    turn+=1
                    print("MOVE Gemini",move)
                else:
                    symbol = "O"
                    move = local_llm_move(board,symbol,model,tokenizer,device)
                    if move >=0 and move<=8:
                        board[move] = symbol
                    turn-=1
                    print("MOVE LLM",move)
                j+=1
                    
                print(board," board")
                if j==9:
                    break
                



                






if __name__ == "__main__":
    main()
