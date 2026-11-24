
import streamlit as st

from chatbot.engine import find_best_match


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="AskWise | FAQ Assistant",
    page_icon="💬",
    layout="centered"
)


# ---------------------------------
# Chatbot configuration
# ---------------------------------

st.title("💬 AskWise")
st.caption("Your intelligent e-commerce support assistant")

st.markdown(
    "Hello! 👋 I'm AskWise. Ask me anything about "
    "orders, delivery, returns, refunds and payments."
)


# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:
    st.header("About AskWise")

    st.write(
        "AskWise uses Natural Language Processing "
        "to understand your questions and find "
        "the most relevant FAQ answer."
    )

    st.divider()

    st.subheader("Try asking")

    st.markdown("""
    - Where is my order?
    - How can I get a refund?
    - Can I pay using UPI?
    - How do I cancel my order?
    - What if my product is damaged?
    """)

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------
# Initialize chat history
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------
# Display previous messages
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show matching score only for debugging
        if message.get("similarity") is not None:
            st.caption(
                f"FAQ similarity: "
                f"{message['similarity']:.2%}"
            )


# ---------------------------------
# Process new user question
# ---------------------------------

if user_question := st.chat_input(
    "Ask your question here..."
):

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Find matching FAQ
    result = find_best_match(user_question)

    # Generate chatbot response
    if result:
        bot_response = result["answer"]
        similarity = result["similarity"]

    else:
        bot_response = (
            "I'm sorry, I couldn't find a suitable answer "
            "to your question. Please try rephrasing it "
            "or ask about orders, delivery, refunds, "
            "returns or payments."
        )
        similarity = None

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

        if similarity is not None:
            st.caption(
                f"FAQ similarity: {similarity:.2%}"
            )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "similarity": similarity
    })
