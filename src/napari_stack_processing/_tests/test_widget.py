from napari_stack_processing import deinterleave_widget


def test_deinterleave_widget():
    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = deinterleave_widget()

    assert my_widget is not None
