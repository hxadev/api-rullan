from flask import Flask, send_file, send_from_directory, Response
from flask_restful import Api, Resource
from ReporteMaker import ReporteMaker

app = Flask(__name__)
api = Api(app)


class Reportes(Resource):

    def status(self):
        return {"status": "ok"}

    def get(self, id):
        reporte = ReporteMaker(id).generarReporte()

        # return Response(
        #                 mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        #                 headers={'Content-Disposition': "attachment;filename={}".format(reporte)})

        return send_file(reporte, as_attachment=True)
        # return {"status": "ok", "data": reporte}

    def post(self, id):

        return


api.add_resource(Reportes, "/reportes/<int:id>/<string:fecha>")


if __name__ == "__main__":
    app.run(host='192.168.0.9', debug=True)
