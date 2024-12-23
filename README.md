# Meteo.lt Forecast Integration for Home Assistant

This is a custom integration for Home Assistant that provides weather forecast data from the official Lithuanian Hydrometeorological Service (LHMT) API - Meteo.lt.

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

## Prerequisites

Before installing this integration, make sure:

- You have Home Assistant installed
- You have HACS (Home Assistant Community Store) installed
- Your Home Assistant instance is running in Lithuania or you're interested in Lithuanian weather forecasts

## Installation

### Option 1: Installation via HACS (Recommended)

1. In HACS, click the three dots in the top right corner and select "Custom repositories"
2. Add this repository URL with category "Integration"
3. Click "Install"
4. Restart Home Assistant

### Option 2: Manual Installation

1. Download the latest release
2. Copy the `custom_components/meteoltforecast` folder to your Home Assistant's `custom_components` folder
3. Restart Home Assistant

## Configuration

1. Go to Home Assistant Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Meteo.lt Forecast"
4. Select your location from the dropdown list (closest location to your Home Assistant coordinates will be selected by default)
5. Click "Submit"

## Usage

After configuration, the integration will create a weather entity that you can use in:

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

This integration uses the official LHMT (Lithuanian Hydrometeorological Service) API. Data is provided under the Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) license. When using the data, please attribute: "Data source: LHMT".

## API Rate Limits

The API has the following rate limits:

- Maximum 180 requests per minute from one IP address
- Maximum 20,000 requests per day from one IP address

The integration is configured to update data every 30 minutes by default to stay well within these limits.

## Troubleshooting

Common issues and solutions:

1. **Integration not showing up in Home Assistant:**

   - Make sure you've restarted Home Assistant after installation
   - Check your Home Assistant logs for any errors

2. **No forecast data:**

   - Verify your internet connection
   - Check if meteo.lt website is accessible
   - Check Home Assistant logs for API errors

3. **Wrong location:**
   - Remove the integration
   - Add it again and manually select your preferred location

## Contributing

Feel free to contribute to this project by:

- Reporting bugs
- Suggesting improvements
- Creating pull requests
- Providing feedback

## Disclaimer

This integration is provided "as is", without warranty of any kind, express or implied. The creator takes no responsibility for any damages that might occur from the use of this integration. Use at your own risk.

Please note that this is a third-party integration and is not officially supported by LHMT or Home Assistant. The integration may stop working if the LHMT API changes.

## License

This project is licensed under CC BY-SA 4.0 - see the LICENSE file for details.
