from flask import Blueprint, render_template
import psycopg2
import os

providers_bp = Blueprint('providers', __name__, template_folder='templates')

@providers_bp.route('/providers')
def providers():
    return render_template('providers.html')

@providers_bp.route('/networks')
def networks():
    database_url = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    cur.execute("SELECT network_id, code, name FROM networks ORDER BY network_id")
    networks = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('networks.html', networks=networks)