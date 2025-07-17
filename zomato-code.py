from flask import Flask,jsonify,request,render_template
import mysql.connector

app=Flask(__name__)

def cont():
    return mysql.connector.connect(host='localhost',database='zomato',user='root',password='keerthi@0330kamalesh')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/place_order',methods=["POST"])
def p_order():
    connection=None
    cursor=None
    try:
        o_data=request.get_json()
        cart=o_data['cart']
        address=o_data['address']

        connection=cont()
        cursor=connection.cursor()

        for i in cart:
            item_name=i['name']
            quantity=i['quantity']

            cursor.execute("select item_id from items where item_name=%s",(item_name,))
            r=cursor.fetchone()
            if r:
                item_id=r[0]
                user_id=1
                query="insert into orders(user_id,item_id,quantity,delivery_address) values(%s, %s, %s, %s)"
                cursor.execute(query,(user_id,item_id,quantity,address))

            else:
                return jsonify({"error":f"item '{item_name}' is not found"}),200
        connection.commit()
        return jsonify({"message":"order placed successfully"}),200

    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

@app.route('/order_details',methods=["GET"])
def o_get():
    connection=None
    cursor=None
    try:
        connection=cont()
        cursor=connection.cursor()
        cursor.execute("select * from orders")
        o=cursor.fetchall()
        return jsonify(o)
    except Exception as e:
        return jsonify({"Error":str(e)}),500
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

if __name__=="__main__":
    app.run(debug=True,port=5001)