import cutlet
katsu = cutlet.Cutlet()

# comparison
nkatu = cutlet.Cutlet('nihon')

sent = "彼女は王への手紙を読み上げた。"
katsu.romaji(sent)
# => 'Kanojo wa ou e no tegami wo yomiageta.'
nkatu.romaji(sent)
# => 'Kanozyo ha ou he no tegami wo yomiageta.'