# Meteo.lt Forecast Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

This is a custom integration for Home Assistant that provides weather forecast data from the official Lithuanian Hydrometeorological Service (LHMT) API - Meteo.lt.

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Click the three dots in the top right corner and select "Custom repositories"
   - Add `https://github.com/moonia33/meteoltforecast`
   - Select category "Integration"
3. Click "Install"
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/meteoltforecast` folder to your Home Assistant's `custom_components` folder
2. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Click "+ ADD INTEGRATION"
3. Search for "Meteo.lt Forecast"
4. Select your location from the dropdown list (closest location to your Home Assistant coordinates will be selected by default)
5. Click "Submit"

## Features

- Hourly weather forecasts up to 7 days
- Automatic location selection based on Home Assistant's configured location
- Real-time weather conditions including:
  - Temperature
  - Feels like temperature
  - Air pressure
  - Humidity
  - Wind speed and direction
  - Precipitation
  - Cloud coverage
  - Weather conditions
- Local time zone support (automatically converts UTC to Europe/Vilnius)
- Compatible with Home Assistant's standard weather cards and dashboards

## Example Usage

You can use this integration in:

- Weather cards
- Weather dashboard
- Automations
- Templates
- Sensors

Example weather card configuration:

```yaml
type: weather-forecast
entity: weather.meteoltforecast_your_location
```

## API Attribution

This integration uses the official LHMT (Lithuanian Hydrometeorological Service) API. Data is provided under the Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) license.

[![Add Integration to your Home Assistant instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=meteoltforecast)

## API Limitations

- Maximum 180 requests per minute from one IP address
- Maximum 20,000 requests per day from one IP address

The integration is configured to update data every 30 minutes by default to stay well within these limits.

## Troubleshooting

### Common Issues

1. **Integration not showing up:**

   - Make sure you've restarted Home Assistant after installation
   - Check your Home Assistant logs for any errors

2. **No forecast data:**

   - Verify your internet connection
   - Check if meteo.lt website is accessible
   - Check Home Assistant logs for API errors

3. **Wrong location:**
   - Remove the integration
   - Add it again and manually select your preferred location

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under CC BY-SA 4.0 - see the LICENSE file for details.

## Disclaimer

This integration is provided "as is", without warranty of any kind. The creator takes no responsibility for any damages that might occur from its use. Use at your own risk.
