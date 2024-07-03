class AlgorithmInfo:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"{self.name}: {self.description}"


algorithms = [
    AlgorithmInfo(
        name="pHash",
        description="pHash is the most optimal in terms of accuracy and speed.\nRecommendation: use these algorithms to find similar images faster and more accurately."
    ),
    AlgorithmInfo(
        name="aHash",
        description="aHash is fast, but less resistant to distortion than pHash."
    ),
    AlgorithmInfo(
        name="bHash",
        description="bHash is resistant to local changes in the image, but less resistant to global transformations."
    ),
    AlgorithmInfo(
        name="dHash",
        description="dHash is resistant to brightness changes, but sensitive to image rotation."
    ),
    AlgorithmInfo(
        name="mHash",
        description="mHash is more resistant to changes in brightness and contrast than aHash, and is also more resistant to noise and distortion than pHash."
    ),
    AlgorithmInfo(
        name="ORB",
        description="ORB is the most accurate algorithm, but the slowest. It finds copies of different extensions and is resistant to turns, noise, scaling, cropping, and lighting changes.\nRecommendation: use on a small dataset."
    ),
    AlgorithmInfo(
        name="MD5",
        description="Use on a large amount of data to quickly search for absolutely identical images.\nThe fastest, but least accurate of the MD5 and SHA algorithms."
    ),
    AlgorithmInfo(
        name="SHA-1 (160-bit)",
        description="Use on a large amount of data to quickly search for absolutely identical images.\nAverage in cost and accuracy among MD5 and SHA algorithms."
    ),
    AlgorithmInfo(
        name="SHA-2 (256-bit)",
        description="Use on a large amount of data to quickly search for absolutely identical images.\nAverage in cost and accuracy among MD5 and SHA algorithms."
    ),
    AlgorithmInfo(
        name="SHA-2 (384-bit)",
        description="Use on a large amount of data to quickly search for absolutely identical images.\nAverage in cost and accuracy among MD5 and SHA algorithms."
    ),
    AlgorithmInfo(
        name="SHA-2 (512-bit)",
        description="Use on a large amount of data to quickly search for absolutely identical images.\nThe slowest, but most accurate of the MD5 and SHA algorithms."
    ),
]


def get_algorithm_names():
    return [algorithm.name for algorithm in algorithms]


def get_algorithm_description_by_name(name):
    for algorithm in algorithms:
        if algorithm.name == name:
            return algorithm.description
    return None
