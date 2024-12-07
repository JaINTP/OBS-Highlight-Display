# OBS Chat Highlight Display

A sleek application to showcase highlighted chat messages from a Twitch stream directly in OBS. Designed to simplify engagement tracking by presenting chat highlights in a customizable and stylish interface.

---

## Use Case

This tool enables streamers to:

1. Automatically highlight important chat messages (e.g., mentions, specific keywords).
2. Display chat highlights in a visually appealing format.
3. Seamlessly integrate with OBS as a custom dock or browser source.

---

## Features

- **OAuth2 Authentication:** Secure Twitch login flow with token management.
- **Customizable Chat Display:** Stylish and responsive UI for chat messages.
- **Real-Time Highlights:** WebSocket integration ensures instant updates.
- **Flexible Configurations:** Supports mentions, nickname matching, and self-messages.
- **OBS Integration:** Optimized for OBS custom docks.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or later.
- OBS Studio installed.

### Setting Up a Twitch Application

1. **Create a New Twitch Application:**

   - Visit [Twitch Developers Console](https://dev.twitch.tv/console/apps).
   - Click **Register Your Application**.
   - Provide the following details:
     - **Name:** A meaningful name for your app.
     - **OAuth Redirect URLs:** Add `http://localhost:3000/`.
     - **Category:** Choose "Chat Bot" or an appropriate category.
   - Save your application and copy the **Client ID**.

2. **Update Permissions:**

   - Ensure the following scopes are included:
     - `chat:read`
     - `chat:edit`

---

### Configuration

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-repo/obs-chat-highlight.git
   cd obs-chat-highlight
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Edit the Configuration File:**
   Open `config.yaml` and update the required fields:

   ```yaml
   client_id: your_client_id
   redirect_uri: http://localhost:3000/
   auth_url: https://id.twitch.tv/oauth2/authorize
   token_url: https://id.twitch.tv/oauth2/token
   server_ports:
     auth_server: 3000
     web_server: 5000
   access_token: null
   refresh_token: null
   highlight_timeout: 120000
   allow_non_mentions: false
   process_own_messages: false
   ```
   - **client\_id:** Replace this with the client id you get from the twitch developer console.
   - **allow\_non\_mentions:** Set to `true` to highlight any message containing your username.
   - **process\_own\_messages:** Set to `true` to highlight messages sent by the authenticated user.

4. **Run the Application:**

   ```bash
   python main.py
   ```

5. **Authenticate:**

   - Follow the prompt to log in and authorize the application.

6. **View the Highlights:**

   - Open `http://localhost:5000` to see live chat highlights.

---

## Using in OBS

### Add as a Custom Dock

1. Open OBS Studio.
2. Navigate to **View > Docks > Custom Browser Docks**.
3. Configure a new dock:
   - **Dock Name:** Chat Highlights
   - **URL:** `http://localhost:5000`
4. Click **Apply** and position the dock as needed.

### Add as a Browser Source
###### While it's not really intended to be used as a browser source, I guess you can...

Open OBS Studio.

1. Go to **Sources** and click the `+` button.
2. Select **Browser.**
3. Configure the source:
   - **URL:** `http://localhost:5000`
   - **Width:** 800 (or preferred width).
   - **Height:** 600 (or preferred height).
4. Click **OK.**

---

## Styling the Display

The app's interface is fully customizable via CSS. Styles are located in the `static/` folder.

### Example Customizations

- **Change Username Colors:** Modify the `.username` selector in CSS.
- **Adjust Timer Display:** Update the `.timer` styles.
- **Background Updates:** Change the `background-color` in the `#listbox` selector.

---

## Key Configurations

- **Timeout Duration:** Control message visibility duration with `highlight_timeout`.
- **Mentions and Own Messages:** Fine-tune behavior using `allow_non_mentions` and `process_own_messages`.

---

## Troubleshooting

### Common Issues

- **Authentication Fails:** Check `client_id` and `redirect_uri` in `config.yaml`.
- **Messages Not Displaying:** Ensure the app is running and OBS URL points to `http://localhost:5000`.

---

## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software, provided that you include the original copyright notice in any distribution.
See the `LICENSE` file for details.

---

## Contribution

Contributions are welcome! Submit a pull request to improve functionality or documentation.

---

## Support

For issues or queries, open a ticket on GitHub or contact the repository maintainer.

