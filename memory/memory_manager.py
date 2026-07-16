from database.db import get_connection


def save_chat(
    user_id,
    user_message,
    bot_response,
    sentiment
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (
            user_id,
            user_message,
            bot_response,
            sentiment
        )
        VALUES (?,?,?,?)
        """,
        (
            user_id,
            user_message,
            bot_response,
            sentiment
        )
    )

    conn.commit()
    conn.close()


def get_recent_history(
    user_id,
    limit=5
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        user_message,
        bot_response
        FROM chat_history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    history = cursor.fetchall()

    conn.close()

    return history