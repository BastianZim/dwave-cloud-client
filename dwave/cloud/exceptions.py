# Copyright 2017 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dwave.cloud.api import exceptions as api


# alias for backward compatibility
SAPIError = api.RequestError


class ConfigFileError(Exception):
    """Base exception for all config file processing errors."""

class ConfigFileReadError(ConfigFileError):
    """Non-existing or unreadable config file specified or implied."""

class ConfigFileParseError(ConfigFileError):
    """Invalid format of config file."""


class SolverError(api.RequestError):
    """Generic solver-related error"""

class ProblemError(api.RequestError):
    """Generic problem-related error"""


class SolverFailureError(SolverError):
    """Remote failure calling a solver"""

class SolverNotFoundError(api.ResourceNotFoundError, SolverError):
    """Solver with matching feature set not found / not available"""

class ProblemNotFoundError(api.ResourceNotFoundError, ProblemError):
    """Problem not found"""

class SolverOfflineError(SolverError):
    """Action attempted on an offline solver"""

class SolverAuthenticationError(api.ResourceAuthenticationError, SolverError):
    """Invalid token or access denied"""

class UnsupportedSolverError(SolverError):
    """The solver received from the API is not supported by the client"""

class SolverPropertyMissingError(UnsupportedSolverError):
    """The solver received from the API does not have required properties"""


class Timeout(api.RequestError):
    """Deprecated and unused."""

class PollingTimeout(Exception):
    """Problem polling timed out."""

# for backward compatibility
from dwave.cloud.api.exceptions import RequestTimeout


class CanceledFutureError(Exception):
    """An exception raised when code tries to read from a canceled future."""

    def __init__(self):
        super().__init__("An error occurred reading results from a canceled request")


class InvalidAPIResponseError(api.ResourceBadResponseError):
    """Unexpected response from D-Wave Solver API"""


class InvalidProblemError(ValueError):
    """Solver cannot handle the given binary quadratic model."""


class ProblemUploadError(Exception):
    """Problem multipart upload failed."""
