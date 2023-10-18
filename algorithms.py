"""algos.

app/algorithms.py

# """
from titiler.core.algorithm import BaseAlgorithm
from titiler.core.algorithm import algorithms as default_algorithms

from rio_tiler.models import ImageData

import numpy as numpy
from rasterio import windows


"""algos.

app/algorithms.py

"""
from titiler.core.algorithm import BaseAlgorithm
from titiler.core.algorithm import algorithms as default_algorithms

from rio_tiler.models import ImageData


class Slope(BaseAlgorithm):

    def __call__(self, img: ImageData) -> ImageData:

        # Create output ImageData
        # Read data from the RioTiler ImageData
        data = img.array[0]
        mask = img.mask
        bounds = img.bounds
        transform = img.transform
        print(bounds,transform)

        # Calculate slope using the numpy gradient function
        x, y = numpy.gradient(data)
        slope =  numpy.degrees(numpy.arctan(numpy.sqrt(x * x + y * y)) )

        slope_data= slope.astype(dtype=numpy.uint8)

        # Create a new RioTiler ImageData instance with the calculated slope

        slope_imagedata = ImageData(
            slope_data, 
            mask,
            assets=img.assets,
            crs=img.crs,
            bounds=bounds,
            )

        return slope_imagedata

# default_algorithms is a `titiler.core.algorithm.Algorithms` Object
algorithms = default_algorithms.register(
    {
        "slope": Slope,
    }
)

