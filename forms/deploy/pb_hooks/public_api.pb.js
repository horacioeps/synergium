/// <reference path="../pb_data/types.d.ts" />

/**
 * Public read of one open form by public_id.
 * GET /api/sf/form/{publicId}
 */
routerAdd("GET", "/api/sf/form/{publicId}", (e) => {
  const publicId = e.request.pathValue("publicId");
  if (!publicId || publicId.length < 6) {
    throw new BadRequestError("Invalid form id");
  }

  const rows = e.app.findRecordsByFilter(
    "forms",
    'public_id = {:pid} && status = "open"',
    "",
    1,
    0,
    { pid: publicId }
  );
  if (!rows || rows.length === 0) {
    throw new NotFoundError("Form not found or closed");
  }
  const rec = rows[0];
  return e.json(200, {
    id: rec.id,
    public_id: rec.getString("public_id"),
    title: rec.getString("title"),
    description: rec.getString("description"),
    locale: rec.getString("locale"),
    success_message: rec.getString("success_message"),
    schema: rec.get("schema"),
  });
});
