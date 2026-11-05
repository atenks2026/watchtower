# PRIZE & TAX TRACKER - UGREEN AI NAS HACKATHON 2026
# AHVO2-9 (FI) - Finance & Tax Officer
# Updated for: Watchtower (AI Security Analyzer) entry
# Tanggal: 2026-11-02

---

## 1. PRIZE STRUCTURE (VERIFIED FROM RULES)

| Kategori | Hadiah | Pemenang | Tipe | Syarat Khusus |
|---|---|---|---|---|
| **Gold** | $20,000 | 1 | Cash | Highest total score |
| **Silver** | $10,000 | 1 | Cash | 2nd highest |
| **Bronze** | $6,000 | 1 | Cash | 3rd highest |
| **Most Creative** | $5,000/orang | 2 | Cash | Highest Innovation & Differentiation score |
| **TOTAL** | **$46,000** | **5** | | |

**Payout Method**: Bank transfer atau ship ke alamat pemenang
**Timeline**: Maksimal 60 hari setelah dokumen lengkap diterima
**Eligibility Indonesia**: ✅ Explicitly included (Asia-Pacific list)

---

## 2. TAX ANALYSIS - INDONESIA (VERIFY EACH ROW)

| Kewajiban | Berlaku? | Aturan Dasar | Source (VERIFY) | Date Verified | Action Required |
|---|---|---|---|---|---|
| **SPT Tahunan OP (Hadiah = Penghasilan)** | **YA** | UU PPh Pasal 4 ayat (1) huruf a — hadiah = penghasilan | DJP, pajak.go.id | [TBD] | Siapkan bukti penerimaan (surat resmi UGREEN/Devpost) |
| **PPh Pasal 21 (Non-Karyawan)** | **YA** | Hadiah ke orang pribadi = objek PPh 21, dipotong oleh pemberi (UGREEN/Devpost) | PMK-168/PMK.03/2018 | [TBD] | Minta bukti potong (bukti potong PPh 21) dari payer |
| **PPh Final Hadiah (khusus)** | **CEK** | Apakah ada PMK khusus hadiah lomba? | DJP | [TBD] | Verifikasi apakah tarif final atau tarif progresif |
| **PPN/PPM (Jasa)** | **TIDAK** | Tidak ada jasa berbayar, ini hadiah | - | - | N/A |
| **Pelaporan SPT Tahunan** | **YA** | Masuk ke Lampiran 1721-A1 / 1770 | DJP | [TBD] | Catat di SPT Tahunan tahun penerimaan |

**Catatan Penting**: 
- Jika UGREEN/Devpost **potong PPh 21 di US** → bisa kreditkan di SPT Indonesia (tax treaty)
- Jika **TIDAK dipotong** → wajib setor sendiri & lapor SPT
- **VERIFIKASI WAJIB**: Tarif PPh 21 hadiah non-karyawan saat ini (5%? 15%? progresif?)

---

## 3. TAX ANALYSIS - HOST COUNTRY (US) (VERIFY-CURRENT-RATE)

| Kewajiban | Berlaku? | Rate | Source (VERIFY-CURRENT-RATE) | Date Verified | Action Required |
|---|---|---|---|---|---|
| **W-8BEN Form** | **YA** | - | IRS Form W-8BEN | [TBD] | **SIAPKAN SEBELUM MENANG** — submit ke UGREEN/Devpost |
| **Withholding Tax US (Chapter 3)** | **YA** | **15%** (Indonesia-US Tax Treaty Article 21 - Other Income) | IRS Pub 515, Tax Treaty Indonesia-US | [TBD] | Submit W-8BEN untuk claim treaty rate 15% (bukan 30% default) |
| **Backup Withholding** | **JIKA NO W-8BEN** | 24% (US person) / 30% (foreign no treaty) | IRS | [TBD] | Hindari dengan submit W-8BEN tepat waktu |
| **State Tax (California - UGREEN HQ)** | **CEK** | CA tidak punya state tax pada non-resident untuk hadiah? | CA FTB | [TBD] | Verifikasi apakah CA tax applies |

**Tax Treaty Indonesia-US Article 21 (Other Income)**:
- Hadiah lomba = "Other Income" → **15% withholding** (bukan 30%)
- **SYARAT**: Submit **Form W-8BEN** yang valid ke payer (UGREEN/Devpost) **SEBELUM** pembayaran
- Tanpa W-8BEN → 30% withholding (rugi 15%)

---

## 4. ACTION ITEMS UNTUK FOUNDER (SEKARANG)

| # | Aksi | Deadline | Status |
|---|---|---|---|
| 1 | **Download & isi Form W-8BEN** (IRS.gov) | **SEBELUM Round 2 / sebelum menang** | ⏳ PENDING |
| 2 | Siapkan **bukti identitas** (KTP/Paspor) untuk W-8BEN | SEBELUM Round 2 | ⏳ PENDING |
| 3 | Siapkan **bank account details** (SWIFT/BIC, nama bank, nomor rekening) | SEBELUM Round 2 | ⏳ PENDING |
| 4 | Verifikasi **tax residency Indonesia** (NPWP, SKD WPLN jika perlu) | SEBELUM Round 2 | ⏳ PENDING |
| 5 | Minta **bukti potong PPh 21** dari UGREEN/Devpost saat terima hadiah | Saat terima hadiah | ⏳ PENDING |
| 6 | Catat hadiah di **SPT Tahunan OP** tahun penerimaan | Maret tahun berikutnya | ⏳ PENDING |

---

## 5. BUDGET & COST TRACKER (TARGET: $0)

| Item | Estimated Cost | Free Tier? | Actual Cost | Status |
|---|---|---|---|---|
| NVIDIA Nemotron (NIM) | $0 | ✅ Free tier rate-limited | $0 | ✅ READY |
| OpenRouter (fallback) | $0 | ✅ Free tier | $0 | ✅ READY |
| Ollama Local (fallback) | $0 | ✅ Local | $0 | ✅ READY |
| Vercel/Netlify Hosting | $0 | ✅ Free tier | $0 | ✅ READY |
| GitHub Repo | $0 | ✅ Free | $0 | ✅ READY |
| Devpost Registration | $0 | ✅ Free | $0 | ✅ READY |
| Domain (optional) | $10-15/tahun | ❌ Paid | $0 | ⏳ SKIP (not needed) |
| **TOTAL** | **$0** | | **$0** | **✅ CLEAR** |

**Finance Verdict**: **FINANCE: CLEAR** — Zero cost, prize tracker ready, tax checklist prepared.

---

## 6. SCENARIO PLANNING (POST-WIN)

### Jika Menang GOLD ($20,000):
| Item | Amount | Notes |
|---|---|---|
| Gross Prize | $20,000 | |
| US Withholding (15% treaty) | -$3,000 | Butuh W-8BEN valid |
| Net Received | $17,000 | |
| Indonesia PPh 21 (kreditkan US tax) | Per SPT | Gunakan tax credit (Pasal 24 UU PPh) |

### Jika Menang MOST CREATIVE ($5,000):
| Item | Amount |
|---|---|
| Gross | $5,000 |
| US Withholding (15%) | -$750 |
| Net | $4,250 |

---

## 7. DIGITAL TAX WATCH (PPN/PPM)

| Layanan Digital Direncanakan | PPN/PPM? | Rate | Source |
|---|---|---|---|
| *Tidak ada layanan berbayar* | - | - | Target biaya $0 |

---

## 8. VERDICT AHVO2-9

**FINANCE: CLEAR** — dengan **ACTION NEEDED** items:

1. **URGENT**: Founder siapkan W-8BEN + supporting docs **SEKARANG** (bukan nanti)
2. **URGENT**: Verifikasi tarif PPh 21 hadiah terkini di DJP/pajak.go.id
3. **MONITOR**: US withholding rate via IRS Pub 515 / tax treaty

**Next Action untuk Founder**: Download Form W-8BEN (irs.gov/forms-pubs/about-form-w-8ben), isi, simpan siap kirim ke UGREEN/Devpost saat diminta.

---

*Dokumen ini living document — update setiap verifikasi baru.*
*AHVO2-9 (FI) — Direct escalation line to Founder active.*