import psycopg2
from config import DB_CONFIG

def get_db_connection():
    """Create a database connection"""
    return psycopg2.connect(**DB_CONFIG)

def get_or_create_player(username):
    """Get or create a player record"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player = cur.fetchone()
        if player:
            return player[0]
        
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
        return player_id
    except Exception as e:
        conn.rollback()
        print(f"DB Error: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def save_game_session(player_id, score, level):
    """Save game session record"""
    if not player_id:
        return
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"DB Error: {e}")
    finally:
        cur.close()
        conn.close()

def get_top_leaderboard(limit=10):
    """Get top scores from leaderboard"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC LIMIT %s
        ''', (limit,))
        return cur.fetchall()
    except Exception as e:
        print(f"DB Error: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_personal_best(username):
    """Get personal best score for a player"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT MAX(gs.score) FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s
        ''', (username,))
        best = cur.fetchone()[0]
        return best if best else 0
    except Exception as e:
        print(f"DB Error: {e}")
        return 0
    finally:
        cur.close()
        conn.close()