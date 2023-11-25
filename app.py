from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/milestones', methods=['GET'])
def milestones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM milestones")
    data = cur.fetchall()
    cur.close()
    milestones_list = []
    for milestones in data:
        milestones_dict = {
            'id': milestones[0],
            'new_progress': milestones[1],
            'date': milestones[2],
            'note': milestones[3]
        }
        milestones_list.append(milestones_dict)
    return jsonify({'milestones': milestones_list})

@app.route('/milestones/details/<int:id>', methods=['GET'])
def detail_milestones(id):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM milestones
        WHERE id=%s
        """, (id,))

    data = cur.fetchall()
    cur.close()

    if not data:
        return jsonify({'message': 'Data tidak ditemukan'}), 404

    milestones_list = []
    for milestones in data:
        milestones_dict = {
            'id': milestones[0],
            'new_progress': milestones[1],
            'date': milestones[2],
            'note': milestones[3]
        }
        milestones_list.append(milestones_dict)

    return jsonify({'milestones': milestones_list})

@app.route('/milestones/create', methods=['POST'])
def create_milestones():
    new_progress = request.form['new_progress']
    date = request.form['date']
    note= request.form['note']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO milestones (new_progress, date, note) VALUES (%s, %s, %s)", (new_progress, date, note))
    mysql.connection.commit() 
    cur.close()
    return jsonify({'message': 'Data Inserted Successfully'})

@app.route('/milestones/delete/<int:id>', methods=['DELETE'])
def delete_milestones(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM milestones WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Record Has Been Deleted Successfully'})

@app.route('/milestones/update/<int:id>', methods=['PUT'])
def update_milestones(id):

    new_progress = request.form['new_progress']
    date = request.form['date']
    note = request.form['note']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE milestones SET new_progress=%s, date=%s, note=%s
        WHERE id=%s
        """, (new_progress, date, note, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data Updated Successfully'})

if __name__ == "__main__":
    app.run(debug=True)

