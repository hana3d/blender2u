import bpy
import operator


def count_collections():
    collections = bpy.data.collections

    total_polygons = 0

    results = {}
    for coll in collections:
        coll_polygons = 0
        for obj in coll.objects:
            if hasattr(obj.data, 'polygons'):
                coll_polygons += len(obj.data.polygons)
            results[coll.name] = coll_polygons
            total_polygons += coll_polygons

    sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

    print('**********************************************************************')
    print('**********************************************************************')
    print('COLLECTIONS POLYGONS COUNT')
    print('TOTAL: ' + str(total_polygons))
    for obj in sorted_results:
        print(str(obj[0]) + ': ' + str(obj[1]) + ' - ' + format(obj[1] * 100 / total_polygons, '.2f') + '%')

    return
