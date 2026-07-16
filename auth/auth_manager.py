import bcrypt

from database.db import get_connection


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def register_user(
    username,
    email,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )
            VALUES (?,?,?)
            """,
            (
                username,
                email,
                hashed_pw
            )
        )

        conn.commit()

        return True

    except Exception as e:

        print(e)

        return False

    finally:

        conn.close()


def login_user(
    username,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        id,
        password_hash
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        user_id = user[0]

        stored_hash = user[1]

        if bcrypt.checkpw(
            password.encode(),
            stored_hash.encode()
        ):

            return user_id

    return None