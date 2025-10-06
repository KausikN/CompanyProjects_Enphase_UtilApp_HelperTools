"""
SiteHelper
"""

# Imports
import os

# Utils Functions
def Utils_JoinLines(lines, join_str="\n"):
    '''
    Utils - Join multiple strings into single string
    '''
    return join_str.join(lines)

# Main Vars
COMMANDS_DATA = {
    "Ruby Bash Commands": {
        "common": {
            "inputs": {
                "ruby_version": {
                    "type": "text",
                    "name": "Ruby Version",
                    "params": {
                        "value": "3.2.2"
                    }
                }
            }
        },
        "commands": [
            {
                "name": "Install new ruby version",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "rbenv install {ruby_version}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Switch to custom ruby version",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "rbenv global {ruby_version}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Switch to system ruby version",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "rbenv global system",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            }
        ],
    },
    "Java Bash Commands": {
        "common": {
            "inputs": {}
        },
        "commands": [
            {
                "name": "Check installed java versions",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "ls ~/.sdkman/candidates/java",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Install new java version",
                "inputs": {
                    "java_version": {
                        "type": "text",
                        "name": "Java Version",
                        "params": {
                            "value": "21.0.2-open"
                        }
                    }
                },
                "output": {
                    "compute": "constant",
                    "value": "sdk install java {java_version}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Switch java version",
                "inputs": {
                    "java_version": {
                        "type": "text",
                        "name": "Java Version",
                        "params": {
                            "value": "21.0.2-open"
                        }
                    }
                },
                "output": {
                    "compute": "constant",
                    "value": "sdk use java {java_version}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Set java version as default",
                "inputs": {
                    "java_version": {
                        "type": "text",
                        "name": "Java Version",
                        "params": {
                            "value": "17.0.15-open"
                        }
                    }
                },
                "output": {
                    "compute": "constant",
                    "value": "sdk default java {java_version}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Java Gradle Build",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "./gradlew clean build",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Java Gradle Test All",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": "./gradlew clean test",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
            {
                "name": "Java Gradle Test Specific",
                "inputs": {
                    "test_path": {
                        "type": "text",
                        "name": "Tests",
                        "params": {
                            "value": "com.enphase.test_repo.TestSuite"
                        }
                    }
                },
                "output": {
                    "compute": "constant",
                    "value": "./gradlew clean test --tests {test_path}",
                    "type": "code",
                    "params": {
                        "language": "bash"
                    }
                }
            },
        ],
    },
    "Rails Console - AppInfo Operations": {
        "common": {
            "inputs": {
                "flag_name": {
                    "type": "text",
                    "name": "Flag Name",
                    "params": {
                        "value": "enho_events_cassandra_ms_config"
                    }
                },
                "flag_value": {
                    "type": "text",
                    "name": "Flag Value",
                    "params": {
                        "value": "true"
                    }
                }
            }
        },
        "commands": [
            {
                "name": "View",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "info = Info::AppInfo.find_by(type: \"{flag_name}\")"
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "Create",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "Info::AppInfo.create(type: \"{flag_name}\", value: \"{flag_value}\")"
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "Update",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "info = Info::AppInfo.find_by(type: \"{flag_name}\")",
                        "info.value = \"{flag_value}\"",
                        "info.save"
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
        ],
    },
    "Rails Console - Redis Operations": {
        "common": {
            "inputs": {
                "key": {
                    "type": "text",
                    "name": "Key Name",
                    "params": {
                        "value": "test"
                    }
                },
            },
        },
        "commands": [
            {
                "name": "Without Encoding - View",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "READER_REDIS_CACHE.get(\"{key}\")",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "Without Encoding - Set",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "REDIS_CACHE.setex(\"{key}\")",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "Without Encoding - Delete",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "REDIS_CACHE.del(\"{key}\")",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "With Encoding - View",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "get_cache(\"{key}\")",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "With Encoding - Set",
                "inputs": {
                    "value": {
                        "type": "text",
                        "name": "Value",
                        "params": {
                            "value": "true"
                        }
                    },
                    "expiry": {
                        "type": "number",
                        "datatype": str,
                        "name": "Expiry",
                        "params": {
                            "value": 300
                        }
                    },
                },
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "set_cache(\"{key}\", \"{value}\", {{:expiry => {expiry}}})",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
            {
                "name": "With Encoding - Delete",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "clear_cache(\"{key}\")",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
        ]
    },
}

"""
Test Object

{
    "Test": {
        "common": {
            "inputs": {
                "test": {
                    "type": "text",
                    "name": "test",
                    "params": {
                        "value": "test"
                    }
                },
            },
        },
        "commands": [
            {
                "name": "Test",
                "inputs": {},
                "output": {
                    "compute": "constant",
                    "value": Utils_JoinLines([
                        "test",
                    ]),
                    "type": "code",
                    "params": {
                        "language": "ruby"
                    }
                }
            },
        ]
    },
}
"""

# Main Functions
def SiteHelper_FormSiteLink(domain, params, session_params):
    '''
    Site Helper - Form Site Link
    '''
    # Init
    LINK = ""
    # Form Link
    ## Substitute params to domain
    LINK = domain.format(**params)
    ## Add Session params
    if len(list(session_params.keys())) > 0:
        session_params_str = {}
        for p in session_params.keys():
            session_param_str = str(session_params[p]).replace(" ", "+") # Replace empty spaces with "+"
            session_params_str[p] = session_param_str
        LINK = LINK + "?" + "&".join([f"{p}={session_params_str[p]}" for p in session_params_str.keys()])

    return LINK

# Run Code