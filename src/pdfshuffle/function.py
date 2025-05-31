

def calculate_fitted_image_size(image_width: int, image_height: int,
                                window_width: int = 0, window_height: int = 0,
                                extend: bool = False
                                ) -> tuple[int, int]:
    """
    Calculate the size of an image fitted into a window while maintaining aspect ratio.
    The image will fit entirely within the window if both dimensions are specified.

    Args:
        image_width: Original width of the image.
        image_height: Original height of the image.
        window_width: Width of the window (0 means not constrained).
        window_height: Height of the window (0 means not constrained).
        extend: увеличивает по максимуму

    Returns:
        Tuple of (width, height) of the fitted image.
    """
    # Handle cases where window dimensions are 0 (unconstrained)
    if window_width == 0 and window_height == 0:
        return image_width, image_height

    if window_width == 0:
        # Only height is constrained
        scale = window_height / image_height
        return int(image_width * scale), window_height

    if window_height == 0:
        # Only width is constrained
        scale = window_width / image_width
        return window_width, int(image_height * scale)

    # Both dimensions are constrained - use min scale to fit entirely within window
    width_scale = window_width / image_width
    height_scale = window_height / image_height
    if extend:
        scale = max(width_scale, height_scale)
    else:
        scale = min(width_scale, height_scale)

    new_width = int(image_width * scale)
    new_height = int(image_height * scale)

    return new_width, new_height