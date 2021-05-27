import time
import datetime as dt
from pprint import pprint
import fields, schemas


def main():
    test_config()
    # test_report()



# ------------------------------- Test Config ------------------------------- #
# --------------------------------------------------------------------------- #
class MpmConfig(schemas.NestedDocument):
    float_parameter   = fields.Float()
    integer_parameter = fields.Integer()


class CcpmConfig(schemas.NestedDocument):
    float_parameter   = fields.Float()
    integer_parameter = fields.Integer()

    # We can nest the MPM config inside the CCPM config like this.
    mpm_config        = fields.NestedDocument(MpmConfig)


class Config(schemas.Table):
    # Currently we can only have a maximum of two keys.
    # - Use 'HASH' for the main partition key.
    # - Use 'RANGE' for an additional sort key.
    __tablekeys__ = dict(project_uuid='HASH', release_uuid='RANGE')

    project_uuid = fields.String()
    release_uuid = fields.String()

    d1_date      = fields.Date()
    d2_date      = fields.Date()

    mpm_config   = fields.NestedDocument(MpmConfig)
    ccpm_config  = fields.NestedDocument(CcpmConfig)


def test_config():
    print('Syncing Table.')
    created = Config.sync_table()

    if created:
        print('Waiting 15 seconds for table to be created.')
        time.sleep(15)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Create root config.
    config = Config(
        project_uuid='project-uuid',
        release_uuid='release-uuid',
        d1_date=dt.date.today(),
        d2_date=dt.date.today() + dt.timedelta(days=14),

    )

    # Create MPM config.
    config.mpm_config = MpmConfig(integer_parameter=1, float_parameter=1.11)

    # Create CCPM config with nested MPM config.
    config.ccpm_config            = CcpmConfig(integer_parameter=2, float_parameter=2.22)
    config.ccpm_config.mpm_config = MpmConfig(integer_parameter=3, float_parameter=3.33)

    # Commit to database.
    config.save()

    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Load Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Currently we can only load a single item at a time, using it's exact key.
    config = Config.get_item(project_uuid='project-uuid', release_uuid='release-uuid')

    config_dict = config.to_dict()
    pprint(config_dict)











# ------------------------------- Test Report ------------------------------- #
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


def populate_prediction_curve(prediction_curve):
    for x in range(5):
        date = dt.date.today() + dt.timedelta(days=x)

        actual_datapoint = DataPoint(date=date, value=x)
        prediction_curve.actual.append(actual_datapoint)

        closure_datapoint = DataPoint(date=date, value=x)
        prediction_curve.predicted.append(closure_datapoint)


def test_report():
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
    report.save()

    # pprint(report.dump())

    # time.sleep(5)
    item = Report.get_item(filter_hash='test-hash')
    item.filter_hash = 'test-123'
    item.save()

    new_item = Report.get_item(filter_hash='test-123')
    print(new_item.to_dict())
    # print(type(item.arrival.predicted[1].date))
    # pprint(item)



if __name__ == '__main__':
    main()
