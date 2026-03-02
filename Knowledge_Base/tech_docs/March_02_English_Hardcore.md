# NIST CSF 2.0 PR.DS & PIPL Article 51 – Hardcore Study Outline

---

## 1. NIST CSF 2.0 – PR.DS Focus (Data Security)

### 1.1 Original Text – PR.DS Subcategories

**PR.DS-01 – Data-at-rest**

> The confidentiality, **integrity**, and availability of **data-at-rest** are protected.

- **Data-at-rest**: data stored on disks, databases, backups, file systems, object storage, etc.
- **Integrity**: protection against unauthorized modification, corruption, or tampering of stored data.
- Typical technical controls: full-disk encryption, database encryption, filesystem permissions, WORM storage, checksums.

---

**PR.DS-02 – Data-in-transit**

> The confidentiality, **integrity**, and availability of **data-in-transit** are protected.

- **Data-in-transit**: data moving over networks (LAN, WAN, Internet, VPN, inter-service RPC, APIs).
- **Integrity**: preventing man-in-the-middle tampering, replay, or packet injection during transmission.
- Typical technical controls: TLS/HTTPS, SSH tunnels, VPNs, message authentication codes (MAC), TLS certificate pinning.

---

**PR.DS-10 – Data-in-use**

> The confidentiality, **integrity**, and availability of data-in-use are protected.

- Data-in-use: data loaded in memory and actively processed by applications, analytics pipelines, or ML models.
- Integrity: ensuring that computations are not altered (e.g., memory corruption, code injection).
- Typical technical controls: hardened runtimes, memory protection, confidential computing/TEE, anti-tamper and runtime integrity checks.

---

## 2. PIPL Article 51 – Security Measures for Personal Information Handling

### 2.1 PIPL Article 51 – English Text (Key Concepts Highlighted)

> Based on the purposes and methods of handling, the types of personal information to be handled, the impact and potential security risks to individuals’ rights and interests,  
> personal information handlers shall take the following measures to ensure that their personal information handling activities comply with the provisions of laws and administrative regulations,  
> and to prevent unauthorized access as well as the leaking, alteration, or loss of personal information:  
>  
> (1) formulating internal security management systems and operating procedures;  
> (2) implementing categorized management of personal information;  
> (3) adopting corresponding technical security measures such as **encryption** and **de-identification**;  
> (4) reasonably determining the **operational authority** for personal information handling, and regularly conducting security education and training for employees;  
> (5) formulating and organizing the implementation of personal information security incident response plans; and  
> (6) other measures as provided for in laws and administrative regulations.

### 2.2 Core Compliance Terms (for technical mapping)

- **Encryption**: cryptographic protection of personal data so that unauthorized parties cannot read it.
- **De-identification**: processing personal data so that it cannot be used to identify a specific individual without additional information.
- **Operational authority / privileges**: scope of what a given account, role, or process is allowed to do when handling personal information (least privilege).

---

## 3. Technical Mapping – Legal Concepts ↔ Linux Commands & Mechanisms

| Legal / Framework Concept                             | Engineering / Linux Mapping Example                                |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| **Data-at-rest** (NIST PR.DS-01)                      | Disk / filesystem encryption (e.g., LUKS), file permissions        |
| **Data-in-transit** (NIST PR.DS-02)                   | `ssh`, `scp`, `curl https://...`, VPN tunnels                      |
| **Integrity** (NIST PR.DS-01 / 02 / 10)               | `sha256sum`, `md5sum`, signed hashes, integrity verification       |
| **Encryption** (PIPL Art. 51(3))                      | `openssl enc`, `gpg`, encrypted volumes / keys in KMS              |
| **De-identification** (PIPL Art. 51(3))               | Hashing or tokenization via `sha256sum`, salted hashes, token maps |
| **Operational authority / privileges** (PIPL Art. 51) | `chmod`, `chown`, `chgrp`, `sudo`, POSIX ACLs                      |
| Classified management of personal information         | Folder-level separation, UNIX groups, separate DB schemas          |
| Incident response plans                               | Log review via `journalctl`, `grep` on logs, `tar` for log arching |
| Preventing unauthorized access                        | Firewall rules (`iptables`, `nft`), SSH key-only auth              |
| Preventing data loss                                  | `rsync` backups, snapshotting, `tar` archives, offsite copies      |

**How to use this table in an interview:**

- Take a legal word (e.g., **encryption**) and immediately tie it to a concrete Linux or infrastructure control.
- Show you understand both the **regulatory expectation** and the **command-level implementation**.

---

## 4. Interview Gold Sentences (English)

1. **“NIST PR.DS-01 and PR.DS-02 require us to protect the confidentiality and integrity of data-at-rest and data-in-transit, which in practice means enforcing strong encryption at the storage layer and TLS for every inter-service connection.”**

2. **“Article 51 of China’s PIPL goes beyond abstract principles by explicitly calling out encryption, de-identification, and reasonable operational privileges, so our Linux hardening must prove that `chmod`, `ssh`, and `sha256sum` are not just available, but embedded into standard operating procedures.”**

3. **“When I design a compliant data platform, I map every legal requirement from NIST PR.DS and PIPL Article 51 to a concrete control — for example, table-level classification, key-managed encryption, hashed identifiers, and least-privilege roles enforced down to the OS level.”**

