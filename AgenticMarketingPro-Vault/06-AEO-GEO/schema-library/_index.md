---
type: schema-index
last_updated: 2026-01-20
tags: [aeo, geo, type/schema]
---

# Schema Library — Index

> Reusable JSON-LD templates per content type. Each template is a separate file in this folder.

## Templates
| File | Schema type | When to use |
|---|---|---|
| organization.md | Organization | Brand entity on homepage/about |
| article.md | Article | All published content |
| faqpage.md | FAQPage | Pages with FAQ sections |
| howto.md | HowTo | Step-by-step guides |
| product.md | Product | Product/service pages |
| review.md | Review | Customer review pages |
| breadcrumb.md | BreadcrumbList | All pages (navigation) |
| person.md | Person | Author pages |
| videoschema.md | VideoObject | Video content |

## Usage rules
- Every page should have ≥1 schema type
- Schema must pass Google Rich Results Test before publish
- `sameAs` field is mandatory for Organization and Person schemas
- Author schema must link to Person schema with `sameAs` to LinkedIn + bio page
