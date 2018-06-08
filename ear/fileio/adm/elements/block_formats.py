from attr import attrs, attrib, Factory
from attr.validators import instance_of, optional
from fractions import Fraction
from ....common import list_of
from .geom import convert_object_position, DirectSpeakerPosition, ObjectPosition
from .main_elements import AudioChannelFormat


@attrs(slots=True)
class BlockFormat(object):
    id = attrib(default=None)
    rtime = attrib(validator=optional(instance_of(Fraction)), default=None)
    duration = attrib(validator=optional(instance_of(Fraction)), default=None)

    def lazy_lookup_references(self, adm):
        pass


@attrs(slots=True)
class MatrixCoefficient(object):
    inputChannelFormat = attrib(default=None, validator=optional(instance_of(AudioChannelFormat)))

    gain = attrib(default=None, validator=optional(instance_of(float)))
    gainVar = attrib(default=None, validator=optional(instance_of(str)))
    phase = attrib(default=None, validator=optional(instance_of(float)))
    phaseVar = attrib(default=None, validator=optional(instance_of(str)))
    delay = attrib(default=None, validator=optional(instance_of(float)))
    delayVar = attrib(default=None, validator=optional(instance_of(str)))

    inputChannelFormatIDRef = attrib(default=None)

    def lazy_lookup_references(self, adm):
        if self.inputChannelFormatIDRef is not None:
            self.inputChannelFormat = adm.lookup_element(self.inputChannelFormatIDRef)
            self.inputChannelFormatIDRef = None


@attrs(slots=True)
class AudioBlockFormatMatrix(BlockFormat):
    outputChannelFormat = attrib(default=None, validator=optional(instance_of(AudioChannelFormat)))
    matrix = attrib(default=Factory(list), validator=list_of(MatrixCoefficient))

    outputChannelFormatIDRef = attrib(default=None)

    def lazy_lookup_references(self, adm):
        if self.outputChannelFormatIDRef is not None:
            self.outputChannelFormat = adm.lookup_element(self.outputChannelFormatIDRef)
            self.outputChannelFormatIDRef = None

        for coefficient in self.matrix:
            coefficient.lazy_lookup_references(adm)


@attrs(slots=True)
class ChannelLock(object):
    maxDistance = attrib(default=None, validator=optional(instance_of(float)))


@attrs(slots=True)
class ObjectDivergence(object):
    value = attrib(validator=instance_of(float))
    azimuthRange = attrib(default=None, validator=optional(instance_of(float)))
    positionRange = attrib(default=None, validator=optional(instance_of(float)))


@attrs(slots=True)
class JumpPosition(object):
    flag = attrib(default=False, validator=instance_of(bool))
    interpolationLength = attrib(default=None, validator=optional(instance_of(Fraction)))


@attrs(slots=True)
class CartesianZone(object):
    minX = attrib(validator=instance_of(float))
    minY = attrib(validator=instance_of(float))
    minZ = attrib(validator=instance_of(float))
    maxX = attrib(validator=instance_of(float))
    maxY = attrib(validator=instance_of(float))
    maxZ = attrib(validator=instance_of(float))


@attrs(slots=True)
class PolarZone(object):
    minElevation = attrib(validator=instance_of(float))
    maxElevation = attrib(validator=instance_of(float))
    minAzimuth = attrib(validator=instance_of(float))
    maxAzimuth = attrib(validator=instance_of(float))


@attrs(slots=True)
class AudioBlockFormatObjects(BlockFormat):
    position = attrib(default=None, validator=instance_of(ObjectPosition), converter=convert_object_position)
    cartesian = attrib(converter=bool, default=False)
    width = attrib(converter=float, default=0.)
    height = attrib(converter=float, default=0.)
    depth = attrib(converter=float, default=0.)
    gain = attrib(converter=float, default=1.)
    diffuse = attrib(converter=float, default=0.)
    channelLock = attrib(default=None, validator=optional(instance_of(ChannelLock)))
    objectDivergence = attrib(default=None, validator=optional(instance_of(ObjectDivergence)))
    jumpPosition = attrib(default=Factory(JumpPosition))
    screenRef = attrib(converter=bool, default=False)
    importance = attrib(default=10, validator=instance_of(int))
    zoneExclusion = attrib(default=Factory(list), validator=list_of((CartesianZone, PolarZone)))


@attrs(slots=True)
class AudioBlockFormatDirectSpeakers(BlockFormat):
    position = attrib(default=None, validator=instance_of(DirectSpeakerPosition))
    speakerLabel = attrib(default=Factory(list))


@attrs(slots=True)
class AudioBlockFormatHoa(BlockFormat):
    equation = attrib(default=None, validator=optional(instance_of(str)))
    order = attrib(default=None, validator=optional(instance_of(int)))
    degree = attrib(default=None, validator=optional(instance_of(int)))
    normalization = attrib(default="SN3D", validator=instance_of(str))
    nfcRefDist = attrib(default=None, validator=optional(instance_of(float)))
    screenRef = attrib(default=False, validator=instance_of(bool))


@attrs(slots=True)
class AudioBlockFormatBinaural(BlockFormat):
    pass
