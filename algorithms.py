from typing import  Callable
from typing import Callable
from titiler.core.algorithm import algorithms as default_algorithms
from titiler.core.factory import TilerFactory
from titiler.core.algorithm import BaseAlgorithm
from titiler.core.algorithm import algorithms as default_algorithms
from rio_tiler.models import ImageData
import numpy as numpy
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


class Hyposometry(BaseAlgorithm):

    #parameters
    threshold: int 

    #metadata
    output_dtype: str = numpy.uint8

    def __call__(self, img: ImageData) -> ImageData:

        data = img.array[0]
        mask =  numpy.logical_and(data >= 0, data < self.threshold)
        masked_data = numpy.ma.masked_array(data - self.threshold, mask)
        bounds = img.bounds

        slope_imagedata = ImageData(
            masked_data.astype(dtype=self.output_dtype), 
            assets=img.assets,
            crs=img.crs,
            bounds=bounds,
            )

        return slope_imagedata



algorithms = default_algorithms.register(
    {
        "slope": Slope,
        "hyposometry":Hyposometry
    }
)

PostProcessParams: Callable = algorithms.dependency
endpoints = TilerFactory(process_dependency=PostProcessParams)
