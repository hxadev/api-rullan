from Reporte import Reporte
import logging as logger
import datetime


class Reporte1(Reporte):
    def __init__(self, mes, anio):
        nombreReporte = "Reporte1_{}".format(
            str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")).rstrip())
        self.qrys = {
            "qryMovimientos": "SELECT mov_id from pre_movimientos where mov_mes=%s and mov_anio=%s limit 1",
            "qryEmpresas": "SELECT emp_nom from pre_empresas where emp_activo=1 and emp_elimina=0",
            "qryEmpresasElimina": "SELECT emp_nom from pre_empresas where emp_activo=1 and emp_elimina=1",
            "qryGrupoCuentas": """ SELECT pre_gpocuentas_gpcue_id,gprep_nom,gpcue_nom 
            FROM gporeportes_gpocuentas,pre_gporeportes,pre_gpocuentas
            where pre_gporeportes_pre_reportes_rep_id=(select rep_id from pre_reportes where rep_num="1") and gpcue_id=pre_gpocuentas_gpcue_id
            and gprep_id=pre_gporeportes_gprep_id
            order by pre_gporeportes_gprep_id,pre_gpocuentas_gpcue_id asc""",
            "qrySaldos1": """ SELECT E.emp_nom,E.emp_elimina,GR.gprep_nom,GC.gpcue_nom,sum(S.sal_ini) as sal_ini
            FROM pre_saldos AS S,pre_empresas AS E,gporeportes_gpocuentas AS GRGC,pre_gporeportes AS GR,
            pre_gpocuentas AS GC,gpocuentas_cuentas AS GCC,pre_cuentas AS C
            WHERE S.sal_anio=%s and S.sal_mes=%s and E.emp_clave=S.sal_empresa and GR.pre_reportes_rep_id=1 AND GRGC.pre_gporeportes_gprep_id=GR.gprep_id AND GC.gpcue_id=GCC.pre_gpocuentas_gpcue_id
            AND GCC.pre_gpocuentas_gpcue_id=GRGC.pre_gpocuentas_gpcue_id AND C.cue_id=GCC.pre_cuentas_cue_id AND C.cue_num=S.sal_cuenta AND C.cue_nat=GC.gpcue_nat
            GROUP BY S.sal_empresa,GR.gprep_id,GCC.pre_gpocuentas_gpcue_id,C.cue_nat"""

        }
        super().__init__(nombreReporte, mes, anio)
        logger.info("Reporte 1")

    def crearEncabezado(self):
        self.worksheet.merge_range(
            "B1:E1", 'VI-A) BALANCE GENERAL POR EMPRESA')
        logger.info("Encabezado creado")

    def crearCuerpo(self):
        result = None
        self.dbCursor.execute(self.qrys.get("qryMovimientos"), ("01", "2019",))
        centerFormat = self.workbook.add_format()
        centerFormat.set_align("center")
        centerFormat.set_border(1)
        centerFormat.set_border_color("#000000")

        leftFormat = self.workbook.add_format()
        leftFormat.set_align("format")
        leftFormat.set_border(1)
        leftFormat.set_border_color("#000000")

        if self.dbCursor.fetchall() is not None:
            # Ejecuta Query de Empresas
            self.dbCursor.execute(self.qrys.get("qryEmpresas"))
            result = self.dbCursor.fetchall()

            for i, empresa in enumerate(result):
                self.worksheet.write(2, i+1, empresa[0], centerFormat)

            self.worksheet.write(2, 6, "TOTALES", centerFormat)

            # Ejecuta query de empresas eliminadas
            self.dbCursor.execute(self.qrys.get("qryEmpresasElimina"))
            result = self.dbCursor.fetchall()
            for i, empresa in enumerate(result):
                self.worksheet.write(2, i+1+6, empresa[0], centerFormat)

            self.worksheet.write(2, 8, "CONSOLIDADO", centerFormat)
            self.worksheet.set_column('B:I', 15)

            # EJECUTA QUERY GRUPO CUENTAS
            self.dbCursor.execute(self.qrys.get("qryGrupoCuentas"))
            result = self.dbCursor.fetchall()

            grupos = [list[1] for list in result]
            grupos_unicos = set(grupos)

            # SE PROCESAN LAS EMPRESAS Y SE AGRUPAN POR EL GRUPO CUENTAS
            empresas = []
            actual = []

            for i_grupo, grupo in enumerate(grupos_unicos):
                for list in result:
                    if list[1] == grupo:
                        actual.append(list[2])

                if i_grupo == 0 or i_grupo == 2:
                    actual.append("SUMA")
                if i_grupo == 1:
                    actual.append("SUMA")
                    actual.append("TOTAL ACTIVO")
                if i_grupo == 3:
                    actual.append("SUMA")
                    actual.append("TOTAL PASIVO Y CAPITAL")

                empresas.append(actual)

        empresas = empresas[0]
        for i, empresa in enumerate(empresas):
            self.worksheet.write(i+3, 0, empresa, centerFormat if empresa == "SUMA" or empresa ==
                                 "TOTAL ACTIVO" or empresa is "TOTAL PASIVO Y CAPITAL" else leftFormat)
            self.worksheet.set_column(0, 0, 30)

        # Ejecuta query Saldos 1
        self.dbCursor.execute(self.qrys.get("qrySaldos1"), ("2019", "01"))
        result = self.dbCursor.fetchall()

        i = 0
        fila = 2
        col = 1

        empresaInicial = result[i][0]
        grupoInicial = result[i][2]
        while i < len(result):
            print(grupoInicial)
            if(empresaInicial == result[i][0]):
                fila += 1
            else:
                empresaInicial = result[i][0]
                fila = 3
                col += 1

            if grupoInicial != result[i][2]:
                self.worksheet.write(fila, col, 0, centerFormat)
                grupoInicial = result[i][2]

            self.worksheet.write(fila, col, result[i][4]/1000, centerFormat)
            i += 1

        self.workbook.close()
        return result
        logger.info("Cuerpo Creado")

    def generar(self):
        self.crearEncabezado()
        self.crearCuerpo()
        logger.info("Reporte Generado")
        return self.nombreReporte
