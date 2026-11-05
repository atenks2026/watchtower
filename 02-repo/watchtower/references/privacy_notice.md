# Privacy Notice - Watchtower
# Face Recognition Opt-in & Data Protection Compliance
# BIPA (Illinois) | GDPR (EU) | UU PDP (Indonesia)

---

## ⚠️ IMPORTANT: FACE RECOGNITION IS OPT-IN ONLY

**Default Setting: FACE RECOGNITION = DISABLED (OFF)**

Watchtower does NOT perform facial recognition by default. All detection is limited to:
- **Person detection** (human vs non-human)
- **Vehicle detection** (car, truck, motorcycle, etc.)
- **Motion detection** (generic movement)
- **Package detection** (delivery parcels)

**NO biometric data is processed, stored, or transmitted unless you explicitly enable Face Recognition module.**

---

## 🔧 HOW TO ENABLE FACE RECOGNITION (Opt-In)

If you want facial recognition capabilities:

1. **Explicit Consent Required**: You must run:
   ```bash
   watchtower config face-recognition enable
   ```

2. **Consent Record**: System will prompt:
   ```
   ⚠️ FACE RECOGNITION OPT-IN REQUIRED
   
   This will:
   - Extract facial embeddings from video footage
   - Store known faces locally on your NAS
   - Match detected faces against known faces
   - Process biometric data as defined by BIPA/GDPR/UU PDP
   
   Data stays 100% LOCAL on your NAS. No cloud upload.
   
   Do you consent? [y/N]:
   ```

3. **Written Consent Logged**: Consent timestamp and version stored in `/Security/.face_recognition_consent.json`

4. **Revocable Anytime**: Disable anytime:
   ```bash
   watchtower config face-recognition disable
   ```
   This deletes all facial embeddings immediately.

---

## 📋 DATA PROCESSING DETAILS

### What Data We Process (Default Mode)
| Data Type | Purpose | Retention | Location |
|-----------|---------|-----------|----------|
| Camera event metadata (timestamp, type, confidence) | Security briefing generation | 30 days (configurable) | NAS local storage |
| Video clips (±30s around events) | Visual verification in briefing | 7 days (configurable) | NAS local storage |
| HTML briefing reports | User review | 90 days (configurable) | NAS local storage |
| Camera authorization tokens | Folder access | Until revoked | NAS local storage |

### What Data We Process (Face Recognition Enabled)
| Data Type | Purpose | Retention | Location |
|-----------|---------|-----------|----------|
| Facial embeddings (128-dim vectors) | Known face matching | Until deleted by user | NAS local storage |
| Face thumbnails (64x64px) | Visual identification in briefing | 30 days | NAS local storage |
| Match confidence scores | Alert prioritization | 30 days | NAS local storage |

### What We NEVER Process
- ❌ Audio recordings
- ❌ License plate recognition (unless explicitly enabled separately)
- ❌ Cloud upload of any footage or metadata
- ❌ Third-party data sharing
- ❌ Advertising or profiling

---

## 🛡️ LEGAL COMPLIANCE

### BIPA (Illinois Biometric Information Privacy Act)
- ✅ **Written consent** required before collecting biometric data
- ✅ **Publicly available policy** (this document)
- ✅ **Retention schedule** published (deleted on disable)
- ✅ **No sale/lease/trade** of biometric data
- ✅ **Reasonable security** (local NAS, encrypted storage)
- ✅ **Private right of action** respected

### GDPR (General Data Protection Regulation - EU)
- ✅ **Lawful basis**: Explicit consent (Article 9.2.a)
- ✅ **Data minimization**: Only facial embeddings, no raw images stored
- ✅ **Storage limitation**: Auto-delete on disable, configurable retention
- ✅ **Right to access**: Export all biometric data via `watchtower export face-data`
- ✅ **Right to erasure**: `watchtower config face-recognition disable` deletes all
- ✅ **Data portability**: Export in standard format (JSON + NPY)
- ✅ **DPO not required**: Processing not core activity, <250 employees
- ✅ **DPIA**: Conducted for face recognition module

### UU PDP (Undang-Undang Pelindungan Data Pribadi - Indonesia)
- ✅ **Consent**: Explicit, informed, specific (Article 13)
- ✅ **Purpose limitation**: Only for security briefing enhancement
- ✅ **Data minimization**: Embeddings only, no raw face images
- ✅ **Retention**: Configurable, default 30 days
- ✅ **Security**: Local NAS, encryption at rest (NAS-level)
- ✅ **Breach notification**: 72-hour notification to Kominfo if breach
- ✅ **User rights**: Access, correction, deletion, portability
- ✅ **Cross-border**: No cross-border transfer (100% local)

---

## 🔐 SECURITY MEASURES

### Data at Rest
- NAS-level encryption (AES-256, NAS-managed)
- File permissions: Owner read/write only (600)
- No world-readable biometric files

### Data in Transit
- No network transmission of biometric data
- Local-only processing (NAS CPU/NPU)
- No API calls to external services

### Access Control
- UGOS folder authorization required
- Per-capability confirmation gates
- No root/sudo required for operation

### Incident Response
- 72-hour breach notification (GDPR Art.33, UU PDP)
- Automated audit logging of all biometric access
- Immediate disable capability: `watchtower emergency-disable`

---

## 👤 USER RIGHTS

| Right | How to Exercise |
|-------|-----------------|
| **Access** | `watchtower export face-data --output face_data.json` |
| **Rectification** | Re-enroll face via `watchtower enroll-face --name "Name"` |
| **Erasure** | `watchtower config face-recognition disable` (immediate) |
| **Portability** | Export includes JSON metadata + NPY embeddings |
| **Restriction** | Disable face recognition (keeps other features) |
| **Objection** | Disable face recognition at any time |
| **Automated Decision Opt-out** | Face recognition is advisory only; no automated actions |

---

## 📞 CONTACT & COMPLAINTS

**Data Controller**: AHVO2 Team (Founder)
**Contact**: Via UGREEN Skills Hub support channel
**Supervisory Authority**: 
- EU: Your national DPA
- Indonesia: Kominfo / PDP Regulator
- Illinois: Illinois Attorney General

**Complaint Process**:
1. Contact us via Skills Hub support
2. We respond within 30 days (GDPR) / 14 days (UU PDP)
3. Escalate to supervisory authority if unresolved

---

## 📝 VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-02 | Initial release for UGREEN AI NAS Hackathon 2026 |

---

## ✅ USER ACKNOWLEDGMENT

By enabling Face Recognition, you acknowledge:

- [ ] You have read this privacy notice
- [ ] You understand face recognition is OPT-IN and OFF by default
- [ ] You consent to biometric data processing as described
- [ ] You understand data stays 100% local on your NAS
- [ ] You know how to disable and delete data at any time
- [ ] You understand your rights under BIPA/GDPR/UU PDP

**Consent Timestamp**: ___________
**Consent Version**: 1.0
**User Signature**: ___________

---

*This notice is part of Watchtower Skill v1.0 for UGREEN AI NAS Hackathon 2026.*
*Last updated: 2026-11-02*