# Blocked resume fixture

This fixture represents a later session that discovers an earlier increment is
not promoted and still has a blocking finding. The correct result is to report
the gate state and stop before defining new implementation scope.
