"""Test schlage lock."""
from unittest.mock import Mock

from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID, SERVICE_LOCK, SERVICE_UNLOCK
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr


async def test_lock_device_registry(
    hass: HomeAssistant, mock_added_config_entry: ConfigEntry
) -> None:
    """Test lock is added to device registry."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(identifiers={("schlage", "test")})
    assert device.model == "<model-name>"
    assert device.sw_version == "1.0"
    assert device.name == "Vault Door"
    assert device.manufacturer == "Schlage"


async def test_lock_services(
    hass: HomeAssistant, mock_lock: Mock, mock_added_config_entry: ConfigEntry
) -> None:
    """Test lock services."""
    await hass.services.async_call(
        LOCK_DOMAIN,
        SERVICE_LOCK,
        service_data={ATTR_ENTITY_ID: "lock.vault_door"},
        blocking=True,
    )
    await hass.async_block_till_done()
    mock_lock.lock.assert_called_once_with()

    await hass.services.async_call(
        LOCK_DOMAIN,
        SERVICE_UNLOCK,
        service_data={ATTR_ENTITY_ID: "lock.vault_door"},
        blocking=True,
    )
    await hass.async_block_till_done()
    mock_lock.unlock.assert_called_once_with()

    await hass.config_entries.async_unload(mock_added_config_entry.entry_id)
