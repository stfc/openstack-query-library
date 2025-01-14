#!/usr/bin/env python3

import cmd
import textwrap
from openstackquery import ServerQuery, UserQuery, ProjectQuery, FlavorQuery, HypervisorQuery

# -----------------------------------------------------------------------
# Base class and resource-specific classes
# -----------------------------------------------------------------------
class QueryBaseCLI:
    """
    Base class for all Query CLI classes.
    Handles property validation and storage.
    """

    # This list of valid properties is meant to be overridden by subclasses
    valid_properties = []

    def __init__(self):
        self.resource_type = None
        # Initialize an empty list of properties
        self.properties = []
        # Initialize a placeholder for the query object (to be set by subclasses)
        self.query = None
        self.project = None
        self.group_by = None

    def validate_properties(self, property_list):
        """
        Check that each property in property_list is valid for the resource.
        """
        # Extract all valid property names (lower-cased for comparison)
        valid_names = [p["name"].lower() for p in self.valid_properties]

        # Prepare a list for invalid properties
        invalid_props = []
        # Iterate through the given property list
        for prop in property_list:
            # If a property is not in the list of valid names, mark it as invalid
            if prop.lower() not in valid_names:
                invalid_props.append(prop)

        # If any invalid properties were found, raise an error
        if invalid_props:
            raise ValueError(
                f"Invalid property(ies): {', '.join(invalid_props)}. "
                f"Valid options are: {', '.join([p['name'] for p in self.valid_properties])}"
            )

    def set_properties(self, property_list):
        """
        Sets the validated properties.
        """
        # Assign the property list to the object's properties
        if property_list == ['*']:
            self.query.select_all()
        else:
            self.properties = property_list
            self.query.select(*self.properties)

    def run(self):
        """
        executes the actual query
        """
        self.query.run(self.project)
        if self.group_by:
            self.query.group_by(self.group_by)
        print(self.query.to_string()) # FIXME !! This should be in a separate method


class ServerQueryCLI(QueryBaseCLI):
    """
    Class representing server queries.
    """
    # Define valid properties for server queries
    valid_properties = [
        {"name": "flavor_id", "return type": "string", "description": "The ID of the Flavor the Server is using"},
        {"name": "hypervisor_name", "return type": "string", "description": "Name of the Hypervisor"},
        {"name": "image_id", "return type": "string", "description": "The ID of the Image the Server is using"},
        {"name": "project_id", "return type": "string", "description": "The ID of the Project"},
        {"name": "created_at", "return type": "string", "description": "Timestamp of creation."},
        {"name": "description", "return type": "string", "description": "User-provided server description."},
        {"name": "desc", "return type": "string", "description": "User-provided server description."},
        {"name": "id", "return type": "string", "description": "Unique ID assigned to the server."},
        {"name": "uuid", "return type": "string", "description": "Unique ID assigned to the server."},
        {"name": "updated_at", "return type": "string", "description": "Last updated timestamp."},
        {"name": "vm_name", "return type": "string", "description": "User-provided name for the server."},
        {"name": "name", "return type": "string", "description": "User-provided name for the server."},
        {"name": "vm_status", "return type": "string", "description": "State of this server."},
        {"name": "status", "return type": "string", "description": "State of this server."},
        {"name": "user_id", "return type": "string", "description": "ID of the owner of the server."},
        {"name": "ips", "return type": "string", "description": "IP addresses associated with the server."},
        {"name": "vm_ips", "return type": "string", "description": "IP addresses associated with the server."},
        {"name": "server_ips", "return type": "string", "description": "IP addresses associated with the server."},
        {"name": "*", "return type": "string", "description": "returns everything"}
    ]

    def __init__(self):
        # Initialize the base class
        super().__init__()
        # Create a ServerQuery object for performing server queries
        self.resource_type = "servers"
        self.query = ServerQuery()


class UserQueryCLI(QueryBaseCLI):
    """
    Class representing user queries.
    """
    # Define valid properties for user queries
    valid_properties = [
        {"name": "project_id", "return type": "string", "description": "The ID for the project which owns the user"},
        {"name": "description", "return type": "string", "description": "The description of this user."},
        {"name": "desc", "return type": "string", "description": "The description of this user."},
        {"name": "email", "return type": "string", "description": "The email address of this user."},
        {"name": "email_addr", "return type": "string", "description": "The email address of this user."},
        {"name": "email_address", "return type": "string", "description": "The email address of this user."},
        {"name": "user_email_address", "return type": "string", "description": "The email address of this user."},
        {"name": "id", "return type": "string", "description": "Unique ID assigned to the user."},
        {"name": "uuid", "return type": "string", "description": "Unique ID assigned to the user."},
        {"name": "name", "return type": "string", "description": "Unique username within the project."},
        {"name": "username", "return type": "string", "description": "Unique username within the project."},
        {"name": "*", "return type": "string", "description": "returns everything"}
    ]

    def __init__(self):
        # Initialize the base class
        super().__init__()
        # Create a UserQuery object for performing user queries
        self.resource_type = "users"
        self.query = UserQuery()


class ProjectQueryCLI(QueryBaseCLI):
    """
    Class representing project queries.
    """
    # Define valid properties for project queries
    valid_properties = [
        {"name": "description", "return type": "string", "description": "Project description."},
        {"name": "desc", "return type": "string", "description": "Project description."},
        {"name": "project_id", "return type": "string", "description": "ID of the project owning the project."},
        {"name": "project_id", "return type": "string", "description": "Unique ID assigned to the project."},
        {"name": "is_project", "return type": "boolean", "description": "Indicates whether the project also acts as a project." },
        {"name": "is_enabled", "return type": "boolean", "description": "Indicates whether users can authorize against this project."},
        {"name": "name", "return type": "string", "description": "Name of the project."},
        {"name": "parent_id", "return type": "string", "description": "ID of the parent project."},
        {"name": "*", "return type": "string", "description": "returns everything"}
    ]

    def __init__(self):
        # Initialize the base class
        super().__init__()
        # Create a ProjectQuery object for performing project queries
        self.resource_type = "projects"
        self.query = ProjectQuery()


class FlavorQueryCLI(QueryBaseCLI):
    """
    Class representing flavor queries.
    """
    # Define valid properties for flavor queries
    valid_properties = [
        {"name": "description", "return type": "string", "description": "Flavor description."},
        {"name": "desc", "return type": "string", "description": "Flavor description."},
        {"name": "disk", "return type": "int", "description": "Size of the disk."},
        {"name": "disk_size", "return type": "int", "description": "Size of the disk."},
        {"name": "ephemeral", "return type": "int", "description": "Size of ephemeral disk attached."},
        {"name": "ephemeral_disk", "return type": "int", "description": "Size of ephemeral disk attached."},
        {"name": "ephemeral_disk_size", "return type": "int", "description": "Size of ephemeral disk attached."},
        {"name": "id", "return type": "string", "description": "Unique ID assigned to the flavor."},
        {"name": "uuid", "return type": "string", "description": "Unique ID assigned to the flavor."},
        {"name": "is_disabled", "return type": "boolean", "description": "True if flavor is disabled, False if not."},
        {"name": "is_public", "return type": "boolean", "description": "True if flavor is public, False if not."},
        {"name": "name", "return type": "string", "description": "Name of the flavor."},
        {"name": "ram", "return type": "int", "description": "Amount of RAM (in MB)."},
        {"name": "ram_size", "return type": "int", "description": "Amount of RAM (in MB)."},
        {"name": "swap", "return type": "int", "description": "Size of swap partition(s)."},
        {"name": "swap_size", "return type": "int", "description": "Size of swap partition(s)."},
        {"name": "vcpu", "return type": "int", "description": "Number of virtual CPUs."},
        {"name": "vcpus", "return type": "int", "description": "Number of virtual CPUs."},
        {"name": "*", "return type": "string", "description": "returns everything"}
    ]

    def __init__(self):
        # Initialize the base class
        super().__init__()
        # Create a FlavorQuery object for performing flavor queries
        self.resource_type = "flavors"
        self.query = FlavorQuery()


class HypervisorQueryCLI(QueryBaseCLI):
    """
    Class representing hypervisor queries.
    """
    # Define valid properties for hypervisor queries
    valid_properties = [
        {"name": "current_workload", "return type": "int", "description": "Number of tasks on the hypervisor."},
        {"name": "workload", "return type": "int", "description": "Number of tasks on the hypervisor."},
        {"name": "local_disk_free", "return type": "int", "description": "Free local disk space (in GiB)."},
        {"name": "free_disk_gb", "return type": "int", "description": "Free local disk space (in GiB)."},
        {"name": "local_disk_size", "return type": "int", "description": "Total local disk size (in GiB)."},
        {"name": "local_gb", "return type": "int", "description": "Total local disk size (in GiB)."},
        {"name": "local_disk_used", "return type": "int", "description": "Local disk space allocated (in GiB)."},
        {"name": "local_gb_used", "return type": "int", "description": "Local disk space allocated (in GiB)."},
        {"name": "id", "return type": "string", "description": "ID of the hypervisor."},
        {"name": "uuid", "return type": "string", "description": "ID of the hypervisor."},
        {"name": "host_id", "return type": "string", "description": "ID of the hypervisor."},
        {"name": "ip", "return type": "string", "description": "IP address of the hypervisor's host."},
        {"name": "host_ip", "return type": "string", "description": "IP address of the hypervisor's host."},
        {"name": "memory_free", "return type": "int", "description": "Free RAM (in MiB)."},
        {"name": "free_ram_mb", "return type": "int", "description": "Free RAM (in MiB)."},
        {"name": "memory_size", "return type": "int", "description": "Total RAM size (in MiB)."},
        {"name": "memory_mb", "return type": "int", "description": "Total RAM size (in MiB)."},
        {"name": "memory_used", "return type": "int", "description": "RAM currently being used (in MiB)."},
        {"name": "memory_mb_used", "return type": "int", "description": "RAM currently being used (in MiB)."},
        {"name": "name", "return type": "string", "description": "Hypervisor Hostname."},
        {"name": "host_name", "return type": "string", "description": "Hypervisor Hostname."},
        {"name": "running_vms", "return type": "int", "description": "Number of running VMs."},
        {"name": "state", "return type": "string", "description": "State of the hypervisor (up or down)."},
        {"name": "status", "return type": "string", "description": "Status of the hypervisor (enabled or disabled)."},
        {"name": "vcpus", "return type": "int", "description": "Number of vCPUs."},
        {"name": "vcpus_used", "return type": "int", "description": "Number of vCPUs in use."},
        {"name": "disabled_reason", "return type": "string", "description": "Reason the hypervisor is disabled, if any."},
        {"name": "uptime", "return type": "string", "description": "The hypervisor's total uptime info."},
        {"name": "*", "return type": "string", "description": "returns everything"}
    ]

    def __init__(self):
        # Initialize the base class
        super().__init__()
        # Create a HypervisorQuery object for performing hypervisor queries
        self.resource_type = "hypervisors"
        self.query = HypervisorQuery()

# -----------------------------------------------------------------------
# The interactive shell (cmd)
# -----------------------------------------------------------------------
class OpenStackShell(cmd.Cmd):
    # Intro message displayed at startup
    intro = (
        "Welcome to the OpenStack interactive shell.\n"
        "Type 'help' or '?' to list commands.\n"
    )

    def __init__(self):
        # Initialize the cmd.Cmd base class
        super().__init__()
        # Store an active resource object (e.g., ServerQueryCLI()) when set
        self.prompt = "> "
        self.query = None

    def loop(self):
        try:
            self.cmdloop()
        except Exception as ex:
            print(ex)
            self.cmdloop()


    def do_help(self, arg):
        """
        Displays help for commands and includes usage for setting project.
        Usage:
          help               - Show general help.
          help set           - Show help for 'set' command usage.
          help set properties
          help set resource
          help set project
          help run              - Show help for 'run' command usage.
        """
        # If no argument is provided, show default help
        if not arg:
            super().do_help(arg)
        else:
            # Convert user input to lower case for easy comparison
            command_help = arg.strip().lower()

            # If the user specifically wants help with "set project", show usage info
            if command_help == "set project":
                print(textwrap.dedent("""\
                    Usage:
                      set project <project_value>

                    Description:
                      - Sets a project value for the currently selected resource.
                      - You must have a resource selected first.
                """))
            # If the user wants help on "set properties"
            elif command_help == "set properties":
                if self.query is None:
                    print("You must set a resource first before setting properties.\n")
                    print(textwrap.dedent("""\
                        Usage:
                          set properties <prop1, prop2, ...>

                        Description:
                          - Sets properties on the currently selected resource.
                          - Properties must be valid for that resource.
                          - Comma-separated, whitespace is ignored.
                    """))
                else:
                    print("Valid properties for the current resource:")
                    for prop_dict in self.query.valid_properties:
                        print(
                            f"  {prop_dict['name']} "
                            f"[type: {prop_dict['return type']}] - "
                            f"{prop_dict['description']}"
                        )
            # If the user wants help on "set resource"
            elif command_help == "set resource":
                print(textwrap.dedent("""\
                    Usage:
                      set resource <servers|users|projects|flavors|hypervisors>

                    Description:
                      - Selects the type of resource you want to work with.
                """))

            # If the user wants help on "run"
            elif command_help == "run":
                print(textwrap.dedent("""\
                    Usage:
                      run

                    Description:
                      - Executes the query based on previously set resource and project.
                      - Must be called after 'set resource' and 'set project'.
                      - If resource or project is not set, an error is shown.
                """))

            else:
                # Fallback to standard help
                super().do_help(arg)


    def do_set(self, arg):
        """
        Set a resource or set properties for the currently selected resource.

        Usage:
          set resource <servers|users|projects|flavors|hypervisors>
          set properties <comma_separated_list_of_properties>
          set project
        """
        # Split arguments on the first space
        args = arg.split(None, 1)
        # If we don't have enough arguments, show an error
        if len(args) < 2:
            print("Invalid usage. Try: help set")
            return

        # The first part should be either "resource" or "properties"
        mode = args[0].lower()
        options = args[1].strip()

        # Depending on which command was used, call the appropriate method
        if mode == "resource":
            self._set_resource(options)
        elif mode == "properties":
            self._set_properties(options)
        elif mode == "project":
            self._set_project(options)
        else:
            print("Unknown set command. Try: help set")

    def _set_resource(self, resource_name):
        # Convert resource name to lowercase
        resource_name = resource_name.lower()
        # Map resource names to their respective CLI classes
        resource_map = {
            "servers": ServerQueryCLI,
            "users": UserQueryCLI,
            "projects": ProjectQueryCLI,
            "flavors": FlavorQueryCLI,
            "hypervisors": HypervisorQueryCLI,
        }
        # If the resource is invalid, notify the user
        if resource_name not in resource_map:
            print(
                "Invalid resource. Valid options are: "
                "servers, users, projects, flavors, hypervisors."
            )
            return

        # Instantiate the appropriate class and assign it
        self.query = resource_map[resource_name]()
        print(f"Resource set to {resource_name}.")
        self.prompt = f'{self.query.resource_type}/> '

    def _set_properties(self, props_str):
        # If no resource is currently set, inform the user
        if self.query is None:
            print(
                "ERROR: No resource set. Please set a resource before setting properties."
            )
            return

        # Split the properties by comma and strip any whitespace
        prop_list = [p.strip() for p in props_str.split(",") if p.strip()]

        # If no properties were provided, just inform the user
        if not prop_list:
            print("No properties provided.")
            return

        # Validate the provided properties using the query object
        try:
            self.query.validate_properties(prop_list)
            self.query.set_properties(prop_list)
            print(f"Properties set to: {', '.join(self.query.properties)}")
        except ValueError as e:
            print("ERROR:", e)


    def _set_project(self, project_str):
        """
        Sets the project for the currently selected resource by updating
        the `project` attribute in the QueryBaseCLI instance.

        :param project_str: The project value to set.
        """
        # Check if a resource has been set first
        if self.query is None:
            # If no resource is selected, print an error and return
            print("ERROR: No resource set. Please set a resource before setting project.")
            return

        # Assign the project value to the current query object's project attribute
        self.query.project = project_str

        # Confirm that the project has been set
        print(f"Project set to: {project_str}")
        self.prompt = f'{self.query.resource_type}/{self.query.project}/> '

    def do_group_by(self, arg):
        self._group_by(arg)

    def _group_by(self, arg):
        self.query.group_by = arg

   
    def do_select(self, arg):
        """
        Handles the 'select' command with a simplified SQL-like syntax using regular expressions.
        Possible formats:
          select <properties> from <project>
          select <properties> from <project> where <condition>
          select <properties> from <project> group <rule>
          select <properties> from <project> where <condition> group <rule>
        """
        properties = None
        project = None
        where_rule = None
        group_by_rule = None

        parts = arg.split(' group_by ')
        if len(parts) == 2:
            group_by_rule = parts[1]
        arg = parts[0]

        parts = arg.split(' from ')
        properties = parts[0]
        project = parts[1]

        self._set_properties(properties)
        self._set_project(project)
        if group_by_rule:
            self._group_by(group_by_rule)
        self.do_run(arg)



    def do_run(self, arg):
        """
        Executes the 'run' command, which triggers self.query.run() if
        both resource and project have been set.
        """
        # If no resource has been selected, print an error
        if self.query is None:
            print("ERROR: No resource set. Please run 'set resource' before 'run'.")
            return

        # If the project attribute is not set in the query object, print an error
        if not getattr(self.query, "project", None):
            print("ERROR: No project set. Please run 'set project' before 'run'.")
            return

        # Otherwise, execute the query's run method
        # (Assuming the underlying query object has a run() method)
        self.query.run()
        print("Query run successfully.")

#    def do_list(self, arg):
#        print("foo")
#
#    def help_list(self):
#        print("This is the help for list")

    def do_quit(self, arg):
        """Quit the shell."""
        print("Quitting the OpenStack shell...")
        return True

    def do_q(self, arg):
        """Alias for quit."""
        return self.do_quit(arg)

    def emptyline(self):
        # Override the emptyline method
        # Simply return without doing anything
        return

if __name__ == '__main__':
    #OpenStackShell().cmdloop()
    OpenStackShell().loop()

