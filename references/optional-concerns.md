# Optional architecture concerns

Load this reference only when the requirements activate plugins, extension
composition, version coexistence, process isolation, hot replacement or dynamic
unloading. These are not default rearchitecture requirements.

## Extension composition

When plugin or extension composition is in scope, define:

- multiplicity and whether multiple instances are valid;
- authority, registration and construction ownership;
- cleanup and restart behavior;
- version compatibility and update/removal rules;
- isolation, crash and security boundaries;
- preservation of durable domain facts.

Do not turn every module into a plugin. Do not infer domain completion or destroy
domain entities when an extension is removed.

## Version and isolation claims

Do not promise live replacement, conflicting implementations or crash/security
isolation without an explicit process and recovery design. Never blindly retry
an external effect with an unknown outcome.

If the host is Python and the design requires conflicting versions of a
top-level package in one interpreter or unloading imports, define a process
boundary and restart/recovery behavior. Module reload does not provide safe
isolation or version coexistence.

