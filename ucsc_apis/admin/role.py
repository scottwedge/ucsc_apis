# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module performs the operation related to role.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def role_create(handle, name, priv, descr=None, **kwargs):
    """
    creates a role

    Args:
        handle (UcscHandle)
        name (string): role name
        priv (comma separated string): role privilege
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaRole: Managed Object

    Example:
        role_create(handle, name="test_role", priv="admin")

    """

    from ucscsdk.mometa.aaa.AaaRole import AaaRole

    mo = AaaRole(parent_mo_or_dn=ucsc_base_dn,
                 name=name,
                 priv=priv,
                 descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def role_get(handle, name):
    """
    Gets a role

    Args:
        handle (UcscHandle)
        name (string): role name

    Returns:
        AaaRole: Managed Object OR None

    Example:
        role_create(handle, name="test_role")
    """

    dn = ucsc_base_dn + "/role-" + name
    return handle.query_dn(dn)


def role_exists(handle, name, **kwargs):
    """
    checks if a role exists

    Args:
        handle (UcscHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        role_exists(handle, name="test_role", priv="read-only")
    """

    mo = role_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def role_modify(handle, name, **kwargs):
    """
    modifies role

    Args:
        handle (UcscHandle)
        name (string): role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaRole: Managed Object

    Raises:
        UcscOperationError: If AaaRole is not present

    Example:
        role_modify(handle, name="test_role", priv="read-only")
    """

    mo = role_get(handle, name)
    if not mo:
        raise UcscOperationError("role_modify",
                                 "Role does not exist")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def role_delete(handle, name):
    """
    deletes role

    Args:
        handle (UcscHandle)
        name (string): role name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaRole is not present

    Example:
        role_delete(handle, name="test_role")
    """

    mo = role_get(handle, name)
    if mo is None:
        raise UcscOperationError("role_delete",
                                 "Role does not exist")

    handle.remove_mo(mo)
    handle.commit()
