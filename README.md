Endless Sky bindings for Python

$ pip install endless-sky-bindings

```
>>> import endless_sky_bindings as es
>>> es.GameData.BeginLoad(['foo', '--resources', '/Users/tomb/endless-sky/'])
True
>>> ships = es.GameData.Ships()
>>> shuttle = ships.Find("Shuttle")
>>> shuttle.
shuttle.Attributes(      shuttle.Description(     shuttle.Name(
shuttle.BaseAttributes(  shuttle.FinishLoading(   shuttle.Place(
shuttle.ChassisCost(     shuttle.FlightCheck(     shuttle.Recharge(
shuttle.Cost(            shuttle.ModelName(       shuttle.SetName(
>>> shuttle.ChassisCost()
180000
```
