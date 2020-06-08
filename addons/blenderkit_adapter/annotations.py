import copy
import bpy
import blenderkit


def change_annotations(class_, original_annotations, change_function, assigned_property=None):
    if getattr(class_, "is_registered"):
        annotations = copy.deepcopy(original_annotations)

        change_function(annotations)

        class_.__annotations__ = annotations

        bpy.utils.unregister_class(class_)
        bpy.utils.register_class(class_)

        if assigned_property is not None:
            exec(f'{assigned_property}=bpy.props.PointerProperty(type={class_.__module__}.{class_.__name__})')


def restore_annotations(class_, original_annotations, assigned_property=None):
    if getattr(class_, "is_registered"):
        class_.__annotations__ = original_annotations

        bpy.utils.unregister_class(class_)
        bpy.utils.register_class(class_)

        if assigned_property is not None:
            exec(f'{assigned_property}=bpy.props.PointerProperty(type={class_.__module__}.{class_.__name__})')
