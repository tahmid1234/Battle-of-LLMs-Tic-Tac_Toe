import streamlit as st
from game_logic import initialize_board,check_winner
from llm_agent import setup_gemini,gemini_move,get_hf_model_response
import time
board_place_holder = st.empty()
def render_match_info():
    match = st.session_state.match_number
    
    # Alternate who goes first each match
    if match % 2 == 1:
        first_player, second_player = "Gemini", "Meta-LLMA"
        first_symbol, second_symbol = "X", "O"
    else:
        first_player, second_player = "Meta-LLMA", "Gemini"
        first_symbol, second_symbol = "X", "O"
    
    st.markdown(f"### Match {match}")
    st.markdown(f"**{first_player}** will play the first move with symbol **{first_symbol}**.")
    st.markdown(f"**{second_player}** will play the second move with symbol **{second_symbol}**.")
    
    return first_player, second_player, first_symbol, second_symbol
def render_board(board):
    with board_place_holder.container():
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                symbol = board[idx] if board[idx] != " " else "⬜️"
                cols[col].markdown(f"<h2 style='text-align:center'>{symbol}</h2>", unsafe_allow_html=True)
def main():
    print("Battle!!!!!!!!!!!")
    if "match_number" not in st.session_state:
        st.session_state.match_number = 0
    if "battle_active" not in st.session_state:
        st.session_state.battle_active = False
    


    
    match = 0
    st.set_page_config(page_title="Battle of LLMs: Tic-Tac_Toe",layout="wide")
    st.title("🤖 Battle of LLMs: Tic-Tac-Toe")
    gemini_api = st.text_input("Enter your Gemini API Key:",type="password")
    hf_api = st.text_input("Enter your Hugging Face Token:",type="password")
    # first_player = st.selectbox("Select First Player:",["Gemini","Meta-Llama"])
    if not st.session_state.battle_active:
        if st.button("Start Battle") and gemini_api and hf_api:
            
            st.session_state.battle_active = True
            
            
            

            st.rerun()
    else:
        st.button("Start Battle", disabled=True)
        
        gemini_client  = setup_gemini(gemini_api)
        st.session_state.match_number +=1
        
        first_player, second_player, first_symbol, second_symbol = render_match_info()
        board = initialize_board()
        render_board(board)
        
        turn = 1 if first_player == "Gemini" else 2
        winner = None
        
        
        helper_prompt = ""
        while True:
            if turn == 1 and winner is None:
                symbol = first_symbol
                # print(board," board X")
                move = gemini_move(board,symbol,gemini_client,helper_prompt)
                # print("X move", move)
                helper_prompt+= f"X is placed at index {move} so this is no longer empty"
                board[move] = symbol
                turn+=1
                render_board(board)
                winner = check_winner(board)  

                

                
            elif turn ==2 and winner is None:
                symbol = second_symbol
                # print(board," board O")
                move = get_hf_model_response(board,symbol,hf_api,helper_prompt)
                helper_prompt+= f"O is placed at index {move} so this is no longer empty"
                # print("O move", move)
                
                board[move] = symbol
                turn-=1
                render_board(board)
                winner = check_winner(board)

            if winner is not None:
                    print("Winner", winner)
                    st.session_state.battle_active = False
                    if winner == first_symbol:
                            st.markdown(f'{first_player} has won this match')
                    elif winner == second_symbol:
                            st.markdown(f'{second_player} has won this match')
                    else:
                        st.markdown("Tie")
                    
                    board_place_holder = st.empty()
                    st.rerun()
                    break
            

            
                    
                
 
                



                






if __name__ == "__main__":
    main()
