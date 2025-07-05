package usecase

import (
	"context"

	domainNewsletter "github.com/lrndwy/HXNID-Bot-WhatsApp/go-wa-api/domains/newsletter"
	"github.com/lrndwy/HXNID-Bot-WhatsApp/go-wa-api/infrastructure/whatsapp"
	"github.com/lrndwy/HXNID-Bot-WhatsApp/go-wa-api/validations"
	"go.mau.fi/whatsmeow"
)

type serviceNewsletter struct {
	WaCli *whatsmeow.Client
}

func NewNewsletterService(waCli *whatsmeow.Client) domainNewsletter.INewsletterUsecase {
	return &serviceNewsletter{
		WaCli: waCli,
	}
}

func (service serviceNewsletter) Unfollow(ctx context.Context, request domainNewsletter.UnfollowRequest) (err error) {
	if err = validations.ValidateUnfollowNewsletter(ctx, request); err != nil {
		return err
	}

	JID, err := whatsapp.ValidateJidWithLogin(service.WaCli, request.NewsletterID)
	if err != nil {
		return err
	}

	return service.WaCli.UnfollowNewsletter(JID)
}
