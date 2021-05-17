import time
import datetime as dt
import fields, schemas

# ------------------------------- Demo Models ------------------------------- #
# --------------------------------------------------------------------------- #
class DataPoint(schemas.NestedDocument):
    value = fields.Integer()
    date  = fields.Date()


class PredictionCurve(schemas.NestedDocument):
    actual    = fields.List(DataPoint)
    predicted = fields.List(DataPoint)


class Report(schemas.Table):
    __tablekeys__ = dict(filter_hash='HASH')

    filter_hash   = fields.String()
    arrival       = fields.NestedDocument(PredictionCurve)
    closure       = fields.NestedDocument(PredictionCurve)
    backlog       = fields.NestedDocument(PredictionCurve)



# ---------------------------------- Test ----------------------------------- #
# --------------------------------------------------------------------------- #
def populate_prediction_curve(prediction_curve):
    for x in range(5):
        date = dt.date.today() + dt.timedelta(days=x)

        actual_datapoint = DataPoint(date=date, value=x)
        prediction_curve.actual.append(actual_datapoint)

        closure_datapoint = DataPoint(date=date, value=x)
        prediction_curve.predicted.append(closure_datapoint)


def main():
    print('Syncing Table.')
    created = Report.sync_table()

    if created:
        print('Waiting for Table to be active.')
        time.sleep(15)

    report = Report(
        filter_hash='test-hash',
        arrival=PredictionCurve(),
        closure=PredictionCurve(),
        backlog=PredictionCurve(),
    )

    populate_prediction_curve(report.arrival)
    populate_prediction_curve(report.closure)
    populate_prediction_curve(report.backlog)

    print('Saving Item.')
    save_start = time.time()
    report.save()
    save_end = time.time()

    print('Save Time: {}'.format(save_end - save_start))


if __name__ == '__main__':
    main()
