import skdb, yaml
# OUT: Couldn't import OCC.Utils.DataExchange.STEP: Is pythonOCC installed properly?
lego = skdb.load_package('lego')
lego.load_data()
brick1 = lego.parts[0]
brick2 = lego.parts[0]
print yaml.dump(brick1.options([brick2]))

