function togglemenu(){
    const dropdown =
        document.getElementById('profile-dropdown')
  const arrow =
        document.querySelector('.arrow')
    dropdown.classList.toggle('active')

    arrow.classList.toggle('rotate')
}
