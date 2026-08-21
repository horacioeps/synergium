/// <reference path="../pb_data/types.d.ts" />

/**
 * Email Horacio (or form.notify_email) when a submission is created.
 */
onRecordAfterCreateSuccess((e) => {
  try {
    const submission = e.record;
    // Bulk / Sheet sync: do not email per row (only real web submissions).
    const source = (submission.getString("source") || "").trim();
    if (source === "google") {
      console.log("[synergium-forms] skip notify (source=google)");
      return;
    }

    const formId = submission.get("form");
    if (!formId) return;

    const form = e.app.findRecordById("forms", formId);
    const notify = (form.getString("notify_email") || "").trim();
    if (!notify) {
      console.log("[synergium-forms] no notify_email; skip mail");
      return;
    }

    let answers = submission.get("answers") || {};
    if (typeof answers === "string") {
      try {
        answers = JSON.parse(answers);
      } catch (err) {
        answers = {};
      }
    }
    const title = form.getString("title") || "Form";
    const publicId = form.getString("public_id") || "";
    const name = answers.full_name || answers.name || "(no name)";
    const email = answers.email || submission.getString("respondent_email") || "";
    const whatsapp = answers.whatsapp || "";
    const matchMe = answers.match_me || "";
    const need = JSON.stringify(answers.need_now || "");
    const offer = JSON.stringify(answers.offer_next_months || "");
    const seek = answers.what_you_seek || "";
    const howFound = JSON.stringify(answers.how_found_form || "");
    const consent = JSON.stringify(answers.data_consent || "");
    const orcid = answers.orcid || "";

    const body =
      `New submission on Synergium Forms\n\n` +
      `Form: ${title}\n` +
      `public_id: ${publicId}\n` +
      `source: ${source || "web"}\n` +
      `submission: ${submission.id}\n` +
      `when: ${new Date().toISOString()}\n\n` +
      `Name: ${name}\n` +
      `Email: ${email}\n` +
      `WhatsApp: ${whatsapp}\n` +
      `ORCID: ${orcid}\n` +
      `Data consent: ${consent}\n` +
      `How found form: ${howFound}\n` +
      `Match me?: ${JSON.stringify(matchMe)}\n` +
      `Need NOW: ${need}\n` +
      `Offer: ${offer}\n` +
      `Seek: ${seek}\n\n` +
      `Admin: https://forms.synergium.net/_/\n`;

    const message = new MailerMessage({
      from: {
        address: e.app.settings().meta.senderAddress || "horacio@horacio-ps.com",
        name: e.app.settings().meta.senderName || "Synergium Forms",
      },
      to: [{ address: notify }],
      subject: `[Synergium Forms] ${title} — ${name}`,
      text: body,
    });

    e.app.newMailClient().send(message);
    console.log("[synergium-forms] notify sent to", notify);
  } catch (err) {
    console.error("[synergium-forms] notify failed", err);
  }
}, "submissions");
