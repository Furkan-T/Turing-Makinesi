class TuringMachine:
    def __init__(self):
        # Önce tabloda kullanılacak temel durum değişkenlerini tanımlıyoruz
        self.accept_state = 'KABUL_DURUMU'
        self.reject_state = 'RED_DURUMU'
        self.blank = '_'
        
        # Geçiş tablosu yukarıdaki değişkenleri kullandığı için fonksiyonu en son çağırıyoruz
        self.transitions = self._build_transitions()

    def _build_transitions(self):
        """
        Geçiş fonksiyonunu (Delta) oluşturur. 
        Sadece geçerli geçişler tanımlanmıştır. Tanımsız bir durum+okuma kombinasyonu
        doğrudan makineyi RED durumuna çekecektir.
        """
        transitions = {}
        digits = '0123456789'
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # q0 -> q1: İlk rakam
        for d in digits: transitions[('q0', d)] = ('q1', d, 'R')
        
        # q1 -> q2: İkinci rakam
        for d in digits: transitions[('q1', d)] = ('q2', d, 'R')
        
        # q2 -> q3: İlk büyük harf
        for l in letters: transitions[('q2', l)] = ('q3', l, 'R')
        
        # q3 -> q4: İkinci büyük harf
        for l in letters: transitions[('q3', l)] = ('q4', l, 'R')
        
        # q4 -> q5: Üçüncü rakam (formatın 5. karakteri)
        for d in digits: transitions[('q4', d)] = ('q5', d, 'R')
        
        # q5 -> q6: Dördüncü rakam
        for d in digits: transitions[('q5', d)] = ('q6', d, 'R')
        
        # q6 -> q7: Beşinci rakam
        for d in digits: transitions[('q6', d)] = ('q7', d, 'R')
        
        # q7 -> KABUL: Bitiş kontrolü. 
        # Plakanın tam 7 karakter olduğundan emin olmak için 8. karakterin boşluk '_' olması şarttır.
        transitions[('q7', '_')] = (self.accept_state, '_', 'R')

        return transitions

    def run(self, input_string):
        """
        Makineyi verilen girdi ile çalıştırır ve her adımı ekrana basar.
        """
        # Bantı (tape) oluştur. Girdinin sonuna boşluk sembolleri ekleyerek sonsuz bant hissi veriyoruz.
        self.tape = list(input_string) + [self.blank] * 5
        self.head = 0
        self.state = 'q0'

        print(f"\n{'='*40}")
        print(f"Test Edilen Girdi: {input_string}")
        print(f"{'='*40}")

        step = 1
        # Makine Kabul veya Red durumuna ulaşana kadar çalışır
        while self.state not in [self.accept_state, self.reject_state]:
            read_symbol = self.tape[self.head]
            
            # Konsol çıktısını temiz göstermek için bantın anlamlı kısmını birleştiriyoruz
            tape_display = "".join(self.tape).rstrip('_')
            if not tape_display: 
                tape_display = "[Boş Bant]"

            print(f"Adım {step}:")
            print(f"  Mevcut Durum : {self.state}")
            print(f"  Okunan Sembol: {read_symbol}")

            # Geçiş fonksiyonunda bu durum ve sembol tanımlı mı kontrol et
            if (self.state, read_symbol) in self.transitions:
                new_state, write_symbol, move = self.transitions[(self.state, read_symbol)]
                
                # Geçiş başarılıysa hareket yönünü yazdır
                print(f"  Kafa Hareketi: {move} (Sağ)")
                print(f"  Bant İçeriği : {tape_display}\n")
                
                self.tape[self.head] = write_symbol  # Oku/Yaz 
                self.state = new_state
                self.head += 1  # Kafayı sağa kaydır
            else:
                # Geçiş tanımsızsa makine kilitlenir ve durur
                print(f"  Kafa Hareketi: DUR (Tanımsız Geçiş)")
                print(f"  Bant İçeriği : {tape_display}\n")
                self.state = self.reject_state
            
            step += 1
        
        # Sonucu Yazdır
        if self.state == self.accept_state:
            print(">>> Sonuç: KABUL <<<")
        else:
            print(">>> Sonuç: RED <<<")


# --- Ana Program: Kullanıcı Etkileşimi ---
if __name__ == "__main__":
    tm = TuringMachine()
    
    print("*" * 50)
    print(" TURING MAKİNESİ - ARAÇ PLAKA FORMATI TANIYICI ")
    print("*" * 50)
    print("Format: NNLLNNN (Örn: 55AB123)")
    print("Çıkış yapmak için 'q' tuşuna basıp Enter'a basın.\n")

    while True:
        # Girdiyi kullanıcından alıyoruz [cite: 83, 84]
        kullanici_girdisi = input("Lütfen kontrol edilecek plakayı girin: ").strip()

        # Çıkış kontrolü
        if kullanici_girdisi.lower() == 'q':
            print("\nProgram sonlandırılıyor. İyi çalışmalar!")
            break
            
        # Boş girdi kontrolü
        if not kullanici_girdisi:
            print("Hata: Boş bir değer girdiniz. Lütfen tekrar deneyin.\n")
            continue

        # Turing makinesini çalıştır [cite: 85, 86]
        tm.run(kullanici_girdisi)
        print("\n" + "-" * 50 + "\n")