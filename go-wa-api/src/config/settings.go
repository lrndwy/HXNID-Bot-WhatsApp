package config

import (
	"github.com/aldinokemal/go-whatsapp-web-multidevice/src/pkg/utils"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"go.mau.fi/whatsmeow/proto/waCompanionReg"
)

var (
	AppVersion               = "v6.1.2"
	AppPort                  = "3000"
	AppDebug                 = false
	AppOs                    = "AldinoKemal"
	AppPlatform              = waCompanionReg.DeviceProps_PlatformType(1)
	AppBasicAuthCredential   []string
	AppChatFlushIntervalDays = 7 // Number of days before flushing chat.csv

	McpPort = "8080"
	McpHost = "localhost"

	PathQrCode      = "statics/qrcode"
	PathSendItems   = "statics/senditems"
	PathMedia       = "statics/media"
	PathStorages    = "storages"
	PathChatStorage = "storages/chat.csv"

	DBURI = "file:storages/whatsapp.db?_foreign_keys=on"

	WhatsappAutoReplyMessage       string
	WhatsappWebhook                []string
	WhatsappWebhookSecret                = "secret"
	WhatsappLogLevel                     = "ERROR"
	WhatsappSettingMaxImageSize    int64 = 20000000  // 20MB
	WhatsappSettingMaxFileSize     int64 = 50000000  // 50MB
	WhatsappSettingMaxVideoSize    int64 = 100000000 // 100MB
	WhatsappSettingMaxDownloadSize int64 = 500000000 // 500MB
	WhatsappTypeUser                     = "@s.whatsapp.net"
	WhatsappTypeGroup                    = "@g.us"
	WhatsappAccountValidation            = true
	WhatsappChatStorage                  = true
)

func Init() {
	viper.SetConfigFile(utils.ProjectRoot() + "/.env")
	viper.AutomaticEnv()
	viper.SetDefault("APP_PORT", AppPort)
	viper.SetDefault("APP_DEBUG", AppDebug)
	viper.SetDefault("APP_OS", AppOs)
	viper.SetDefault("APP_PLATFORM", AppPlatform)
	viper.SetDefault("APP_BASIC_AUTH_CREDENTIAL", AppBasicAuthCredential)
	viper.SetDefault("APP_CHAT_FLUSH_INTERVAL_DAYS", AppChatFlushIntervalDays)

	viper.SetDefault("MCP_PORT", McpPort)
	viper.SetDefault("MCP_HOST", McpHost)

	viper.SetDefault("PATH_QR_CODE", PathQrCode)
	viper.SetDefault("PATH_SEND_ITEMS", PathSendItems)
	viper.SetDefault("PATH_MEDIA", PathMedia)
	viper.SetDefault("PATH_STORAGES", PathStorages)
	viper.SetDefault("PATH_CHAT_STORAGE", PathChatStorage)

	viper.SetDefault("DB_URI", DBURI)

	viper.SetDefault("WHATSAPP_AUTO_REPLY_MESSAGE", WhatsappAutoReplyMessage)
	viper.SetDefault("WHATSAPP_WEBHOOK", WhatsappWebhook)
	viper.SetDefault("WHATSAPP_WEBHOOK_SECRET", WhatsappWebhookSecret)
	viper.SetDefault("WHATSAPP_LOG_LEVEL", WhatsappLogLevel)
	viper.SetDefault("WHATSAPP_SETTING_MAX_IMAGE_SIZE", WhatsappSettingMaxImageSize)
	viper.SetDefault("WHATSAPP_SETTING_MAX_FILE_SIZE", WhatsappSettingMaxFileSize)
	viper.SetDefault("WHATSAPP_SETTING_MAX_VIDEO_SIZE", WhatsappSettingMaxVideoSize)
	viper.SetDefault("WHATSAPP_SETTING_MAX_DOWNLOAD_SIZE", WhatsappSettingMaxDownloadSize)
	viper.SetDefault("WHATSAPP_TYPE_USER", WhatsappTypeUser)
	viper.SetDefault("WHATSAPP_TYPE_GROUP", WhatsappTypeGroup)
	viper.SetDefault("WHATSAPP_ACCOUNT_VALIDATION", WhatsappAccountValidation)
	viper.SetDefault("WHATSAPP_CHAT_STORAGE", WhatsappChatStorage)

	if err := viper.ReadInConfig(); err != nil {
		logrus.Warn("Failed to read config file, using default values: ", err.Error())
	}

	AppPort = viper.GetString("APP_PORT")
	AppDebug = viper.GetBool("APP_DEBUG")
	AppOs = viper.GetString("APP_OS")
	AppPlatform = waCompanionReg.DeviceProps_PlatformType(viper.GetInt32("APP_PLATFORM"))
	AppBasicAuthCredential = viper.GetStringSlice("APP_BASIC_AUTH_CREDENTIAL")
	AppChatFlushIntervalDays = viper.GetInt("APP_CHAT_FLUSH_INTERVAL_DAYS")

	McpPort = viper.GetString("MCP_PORT")
	McpHost = viper.GetString("MCP_HOST")

	PathQrCode = viper.GetString("PATH_QR_CODE")
	PathSendItems = viper.GetString("PATH_SEND_ITEMS")
	PathMedia = viper.GetString("PATH_MEDIA")
	PathStorages = viper.GetString("PATH_STORAGES")
	PathChatStorage = viper.GetString("PATH_CHAT_STORAGE")

	DBURI = viper.GetString("DB_URI")

	WhatsappAutoReplyMessage = viper.GetString("WHATSAPP_AUTO_REPLY_MESSAGE")
	WhatsappWebhook = viper.GetStringSlice("WHATSAPP_WEBHOOK")
	WhatsappWebhookSecret = viper.GetString("WHATSAPP_WEBHOOK_SECRET")
	WhatsappLogLevel = viper.GetString("WHATSAPP_LOG_LEVEL")
	WhatsappSettingMaxImageSize = viper.GetInt64("WHATSAPP_SETTING_MAX_IMAGE_SIZE")
	WhatsappSettingMaxFileSize = viper.GetInt64("WHATSAPP_SETTING_MAX_FILE_SIZE")
	WhatsappSettingMaxVideoSize = viper.GetInt64("WHATSAPP_SETTING_MAX_VIDEO_SIZE")
	WhatsappSettingMaxDownloadSize = viper.GetInt64("WHATSAPP_SETTING_MAX_DOWNLOAD_SIZE")
	WhatsappTypeUser = viper.GetString("WHATSAPP_TYPE_USER")
	WhatsappTypeGroup = viper.GetString("WHATSAPP_TYPE_GROUP")
	WhatsappAccountValidation = viper.GetBool("WHATSAPP_ACCOUNT_VALIDATION")
	WhatsappChatStorage = viper.GetBool("WHATSAPP_CHAT_STORAGE")
}
