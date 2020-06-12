from flask import Flask
from flask_jsglue import JSGlue
from flask import render_template, redirect, request, url_for

from controller.StartController import StartController
from controller.MainController import MainController
from model.Logging.JSONEncoder import CustomJSONEncoder

jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)

start_controller = StartController()
main_controller = MainController()


@app.route('/')
def start():
    serial_ports = start_controller.get_serial_ports()
    baudrates = start_controller.get_baudrates()
    return render_template("start.html", serial_ports=serial_ports, baudrates=baudrates)


@app.route('/start_test', methods=['POST'])
def start_test():
    serial_port = request.form.get('port')
    baudrate = request.form.get('baudrate')
    if serial_port and baudrate:
        main_controller.start_test(serial_port, baudrate)
        # TODO: else show the warning pop-up and do not redirect   ---flash in Flask
        return redirect(url_for('index'))


@app.route('/settings', methods=['POST'])
def settings():
    heartbeat_period = int(request.form.get('heartbeat_period'))
    ecc_period = int(request.form.get('ecc_period'))
    if heartbeat_period and ecc_period:
        main_controller.set_heartbeat_period(heartbeat_period)
        main_controller.set_ecc_period(ecc_period)
        return redirect(url_for('index'))
    # TODO: else show the warning pop-up and do not redirect   ---flash in Flask


@app.route('/settings')
def settings_open():
    return render_template("index.html", data_packets=main_controller.get_all_data(),
                           heartbeat_periods=main_controller.get_heartbeat_periods(),
                           ecc_check_periods=main_controller.get_ecc_check_periods(),
                           )
    # TODO: else show the warning pop-up and do not redirect   ---flash in Flask


@app.route('/index')
def index():
    data_packets = main_controller.get_all_data()
    return render_template("index.html", data_packets=data_packets, stopped=main_controller.stopped)


@app.route('/data', methods=['GET'])
def data():
    data_packets = main_controller.get_all_data()
    return CustomJSONEncoder().encode(data_packets)


@app.route('/reset', methods=['GET'])
def reset():
    main_controller.send_rest_request()
    return redirect(url_for('index'))


@app.route('/more_info', methods=['GET'])
def more_info():
    curr_data_id = request.args['curr_data_id']
    curr_data = main_controller.get_data(int(curr_data_id))
    main_controller.curr_data = curr_data
    return render_template("index.html", data_packets=main_controller.get_all_data(),
                           heartbeat_periods=main_controller.get_heartbeat_periods(),
                           ecc_check_periods=main_controller.get_ecc_check_periods(),
                           curr_data=main_controller.curr_data)


@app.route('/com_err')
def com_err():
    return render_template("index.html", com_errors=main_controller.get_com_err())


@app.route('/reset_info')
def reset_info():
    return render_template("index.html", reset_packets=main_controller.get_reset_packets())


@app.route('/mem_err')
def mem_err():
    return render_template("index.html", mem_errors=main_controller.get_mem_err_list())


@app.route('/ecc_check_addresses', methods=['GET'])
def ecc_check_addresses():
    curr_mem_err_id = request.args['curr_mem_err']
    curr_mem_err = main_controller.get_mem_err(int(curr_mem_err_id))
    return render_template("index.html", mem_errors=main_controller.get_mem_err_list(), curr_mem_err=curr_mem_err)


@app.route('/stop_test')
def stop_test():
    main_controller.stop_test()
    return redirect(url_for('index'))


@app.route('/get_correct_percentage', methods=['GET'])
def get_correct_percentage():
    percent = main_controller.get_correct_percentage()
    return str(percent)


if __name__ == '__main__':
    app.run()
