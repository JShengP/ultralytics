# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license


class HUBModelError(Exception):
    """
    Custom exception class for handling errors related to model fetching in Ultralytics YOLO.

    This exception is raised when a requested model is not found or cannot be retrieved.
    The message is also processed to include emojis for better user experience.

    Attributes:
        message (str): The error message displayed when the exception is raised.

    Note:
        The message is automatically processed through the 'emojis' function from the 'ultralytics.utils' package.
    """

    def __init__(self, message="Model not found. Please check model URL and try again."):
        """Create an exception for when a model is not found."""
        super().__init__(emojis(message))


def handle_errors(func):
    """Catch exceptions and display instructions to resolve the error if available."""
    from functools import wraps

    from ultralytics.utils import LOGGER, colorstr

    # Structure: {function_name: {exception_type: custom_message}}
    ERRORS = {
        "Results.verbose": {
            KeyError: "Logging results failed. This is probably due to using the wrong 'task' while loading the model. Make sure you pass the correct task while loading the model: 'model = YOLO(\"yolo11n.pt\", task=\"segment\")'. See https://github.com/ultralytics/ultralytics/issues/16094."
        },
        "InfiniteDataLoader.__init__": {
            RuntimeError: "Initializing dataloader failed. If you're on Windows, try placing your code under a `if __name__== '__main__':` block. See https://github.com/ultralytics/ultralytics/issues/18550."
        },
        "non_max_suppression": {
            NotImplementedError: "Post-processing failed. This is probably because a non-CUDA version of torchvision is installed. Try uninstalling torchvision and reinstalling it based on the guide at https://pytorch.org/get-started/locally/. See https://github.com/ultralytics/ultralytics/issues/18601."
        },
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            func_name = func.__qualname__
            exc_type = type(e)
            message = ERRORS.get(func_name, {}).get(exc_type)
            if message:
                LOGGER.error(f"{colorstr('bold', 'red', 'ERROR:')} {message}")
                LOGGER.info("")
            raise  # re-raise exception

    return wrapper
